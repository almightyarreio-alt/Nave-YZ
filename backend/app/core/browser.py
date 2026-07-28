import asyncio
import io
import json
from multiprocessing import context
from operator import index
import re
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from playwright.async_api import BrowserContext, Page, Playwright, async_playwright, TimeoutError
from pathlib import Path
from dotenv import load_dotenv
import os
import contextvars
from contextlib import asynccontextmanager
from app.core.locks import ReentrantLock

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

class SafeDict(dict):
        def __missing__(self, key):
            return "{" + key + "}"
        
class BrowserRunError(RuntimeError):
    """Raised when a saved flow or profile operation cannot run safely."""


class BrowserManager:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.profiles_dir = self.base_dir / "profiles"
        self.flows_dir = self.base_dir / "flows"
        self.default_profile_name = "Perfil Principal"
        self._playwright: Playwright | None = None
        self._contexts: dict[str, BrowserContext] = {}
        self._pages: dict[str, Page] = {}
        self._lock = asyncio.Lock()
        self.last_execution: dict[str, Any] | None = None
        
        self._variables_var: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar("variables", default=None)
        self._page_locks: dict[str, ReentrantLock] = {}
        self._frames: dict[str, Any] = {}
        self._page_to_profile: dict[str, str] = {}

    @property
    def _variables(self) -> dict[str, Any]:
        d = self._variables_var.get()
        if d is None:
            d = {}
            self._variables_var.set(d)
        return d

    @_variables.setter
    def _variables(self, value: dict[str, Any]) -> None:
        self._variables_var.set(value)

    def register_page(self, page_id: str, page: Page, profile_key: str | None = None) -> None:
        self._pages[page_id] = page
        if profile_key:
            self._page_to_profile[page_id] = profile_key
        
        # Listen for page close to clean up and notify MonitorManager
        page.on("close", lambda *_: asyncio.create_task(self._handle_page_close(page_id)))
        self._register_page_frames(page_id, page)

    def _register_page_frames(self, page_id: str, page: Page) -> None:
        self.register_frame(f"{page_id}_main", page.main_frame)
        for i, frame in enumerate(page.frames):
            if frame != page.main_frame:
                frame_name = frame.name or f"frame_{i}"
                self.register_frame(f"{page_id}_{frame_name}", frame)

    def register_frame(self, frame_id: str, frame: Any) -> None:
        self._frames[frame_id] = frame

    def get_page(self, page_id: str) -> Page | None:
        return self._pages.get(page_id)

    def get_frame(self, frame_id: str) -> Any | None:
        if frame_id in self._frames:
            return self._frames[frame_id]
        for page in self._pages.values():
            if not page.is_closed():
                for frame in page.frames:
                    if frame.name == frame_id or frame.url == frame_id:
                        return frame
        return None

    def is_page_alive(self, page_id: str) -> bool:
        page = self._pages.get(page_id)
        return page is not None and not page.is_closed()

    async def acquire_lock(self, page_id: str) -> None:
        if page_id not in self._page_locks:
            self._page_locks[page_id] = ReentrantLock()
        await self._page_locks[page_id].acquire()

    def release_lock(self, page_id: str) -> None:
        lock = self._page_locks.get(page_id)
        if lock is not None:
            try:
                lock.release()
            except RuntimeError:
                pass

    def get_page_id(self, page: Page) -> str | None:
        for pid, p in self._pages.items():
            if p == page:
                return pid
        return None

    def register_context(self, profile_key: str, context: BrowserContext) -> None:
        self._contexts[profile_key] = context

    def get_context(self, profile_key: str) -> BrowserContext | None:
        return self._contexts.get(profile_key)

    @asynccontextmanager
    async def page_lock(self, page_id: str):
        await self.acquire_lock(page_id)
        try:
            yield
        finally:
            self.release_lock(page_id)

    async def _handle_page_close(self, page_id: str) -> None:
        self._pages.pop(page_id, None)
        self._page_to_profile.pop(page_id, None)
        self._page_locks.pop(page_id, None)
        try:
            from app.monitor.manager import monitor_manager
            await monitor_manager.handle_page_closed(page_id)
        except Exception:
            pass

    def _resolve_variables(self, value):
        """
        Substitui placeholders {variavel} pelos valores armazenados
        em self._variables e pelas variáveis do .env.
        """

        if not hasattr(self, "_variables"):
            self._variables = {}

        load_dotenv(ROOT_DIR / ".env", override=False)

        variables = {
            **dict(os.environ),
            **self._variables,
        }

        if isinstance(value, str):
            return value.format_map(SafeDict(variables))

        if isinstance(value, dict):
            return {
                k: self._resolve_variables(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                self._resolve_variables(v)
                for v in value
            ]

        return value

    def _normalize_value(self, value):
        """
        Converte strings booleanas 'true'/'false' para bool e preserva outros valores.
        """
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized == "true":
                return True
            if normalized == "false":
                return False
        return value

    async def start(self) -> None:
        self._ensure_storage()
        if self._playwright is None:
            self._playwright = await async_playwright().start()

    async def stop(self) -> None:
        for context in list(self._contexts.values()):
            try:
                await context.close()
            except Exception:
                pass
        self._contexts.clear()
        self._pages.clear()

        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

    def list_profiles(self) -> list[dict[str, Any]]:
        self._ensure_storage()
        profiles = []
        for profile_dir in sorted(self.profiles_dir.iterdir(), key=lambda item: item.name.lower()):
            if profile_dir.is_dir() and not profile_dir.name.startswith(".import-"):
                profiles.append(self._read_profile_metadata(profile_dir))
        return profiles

    def create_profile(self, name: str) -> dict[str, Any]:
        self._ensure_storage()
        display_name = self._clean_profile_name(name)
        dir_name = self.sanitize_profile_dir_name(display_name)
        profile_dir = self.profiles_dir / dir_name

        if profile_dir.exists() or self._profile_name_exists(display_name):
            raise FileExistsError(f"Perfil ja existe: {display_name}")

        profile_dir.mkdir(parents=False, exist_ok=False)
        metadata = {
            "name": display_name,
            "created_at": self._iso_timestamp(),
            "last_used": None,
            "default": not self.list_profiles(),
        }
        self._write_profile_metadata(profile_dir, metadata)
        if metadata["default"]:
            self._set_only_default(profile_dir)
        return {"profile": metadata, "logs": [self._log("info", f"Perfil criado: {display_name}")]}

    async def open_profile(self, name: str) -> dict[str, Any]:
        async with self._lock:
            await self.start()
            context, page, metadata, profile_dir = await self._get_or_create_context(name)
            metadata = self._touch_profile(profile_dir)
            logs = [self._log("info", f"Perfil aberto: {metadata['name']}")]
            return {
                "status": "success",
                "profile": metadata,
                "url": page.url,
                "active_browsers": self.active_browsers,
                "logs": logs,
            }

    async def rename_profile(self, profile_name: str, new_name: str) -> dict[str, Any]:
        async with self._lock:
            self._ensure_storage()
            profile_dir = self._find_profile_dir(profile_name)
            metadata = self._read_profile_metadata(profile_dir)
            display_name = self._clean_profile_name(new_name)
            target_dir = self.profiles_dir / self.sanitize_profile_dir_name(display_name)

            if metadata["name"].casefold() != display_name.casefold() and self._profile_name_exists(display_name):
                raise FileExistsError(f"Perfil ja existe: {display_name}")
            if target_dir.exists() and target_dir.resolve() != profile_dir.resolve():
                raise FileExistsError(f"Diretorio de perfil ja existe: {target_dir.name}")

            await self._close_profile_context(profile_dir)
            if target_dir.resolve() != profile_dir.resolve():
                profile_dir.rename(target_dir)
                profile_dir = target_dir

            metadata["name"] = display_name
            self._write_profile_metadata(profile_dir, metadata)
            return {"profile": metadata, "logs": [self._log("info", f"Perfil renomeado: {display_name}")]}

    async def delete_profile(self, profile_name: str) -> dict[str, Any]:
        async with self._lock:
            self._ensure_storage()
            profile_dir = self._find_profile_dir(profile_name)
            metadata = self._read_profile_metadata(profile_dir)
            await self._close_profile_context(profile_dir)
            self._safe_rmtree(profile_dir)
            self._ensure_single_default()
            return {"logs": [self._log("info", f"Perfil removido: {metadata['name']}")]}

    def set_default_profile(self, profile_name: str) -> dict[str, Any]:
        self._ensure_storage()
        profile_dir = self._find_profile_dir(profile_name)
        metadata = self._set_only_default(profile_dir)
        return {"profile": metadata, "logs": [self._log("info", f"Perfil padrao definido: {metadata['name']}")]}

    async def export_profile(self, profile_name: str) -> tuple[Path, str, list[dict[str, str]]]:
        async with self._lock:
            self._ensure_storage()
            profile_dir = self._find_profile_dir(profile_name)
            metadata = self._read_profile_metadata(profile_dir)
            await self._close_profile_context(profile_dir)

            export_dir = Path(tempfile.gettempdir()) / "navyauto_exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            zip_name = f"{profile_dir.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
            zip_path = export_dir / zip_name

            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for item in profile_dir.rglob("*"):
                    archive.write(item, (Path(profile_dir.name) / item.relative_to(profile_dir)).as_posix())

            return zip_path, zip_name, [self._log("info", f"Perfil exportado: {metadata['name']}")]

    async def import_profile_zip(self, content: bytes, filename: str | None = None) -> dict[str, Any]:
        self._ensure_storage()
        try:
            archive = zipfile.ZipFile(io.BytesIO(content))
        except zipfile.BadZipFile as exc:
            raise BrowserRunError("Arquivo ZIP invalido.") from exc

        with archive:
            members = archive.infolist()
            self._validate_zip_members(members)
            profile_member = self._find_profile_json_member(members)
            metadata = self._load_imported_metadata(archive.read(profile_member))
            target_dir = self.profiles_dir / self.sanitize_profile_dir_name(metadata["name"])

            if target_dir.exists() or self._profile_name_exists(metadata["name"]):
                raise FileExistsError(f"Perfil ja existe: {metadata['name']}")

            source_parts = PurePosixPath(profile_member.filename).parts
            source_root = source_parts[0] if len(source_parts) > 1 else None
            temp_dir = self.profiles_dir / f".import-{target_dir.name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            try:
                temp_dir.mkdir(parents=False, exist_ok=False)
                for member in members:
                    parts = PurePosixPath(member.filename).parts
                    if source_root and (not parts or parts[0] != source_root):
                        continue
                    rel_parts = parts[1:] if source_root else parts
                    if not rel_parts:
                        continue
                    destination = temp_dir.joinpath(*rel_parts)
                    self._assert_child_path(temp_dir, destination)
                    if member.is_dir():
                        destination.mkdir(parents=True, exist_ok=True)
                    else:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        with archive.open(member) as src, destination.open("wb") as dst:
                            shutil.copyfileobj(src, dst)

                metadata["default"] = not self.list_profiles()
                self._write_profile_metadata(temp_dir, metadata)
                temp_dir.rename(target_dir)
                if metadata["default"]:
                    self._set_only_default(target_dir)
            except Exception:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                raise

        return {"profile": metadata, "logs": [self._log("info", f"Perfil importado: {metadata['name']}")]}

    async def run_flow(self, profile: str, flow: str) -> dict[str, Any]:
        async with self._lock:
            await self.start()
            flow_path = self._resolve_flow_path(flow)
            flow_data = self._load_flow(flow_path)
            steps = self._extract_steps(flow_data)
            context, page, metadata, profile_dir = await self._get_or_create_context(profile)
            metadata = self._touch_profile(profile_dir)

            logs = [self._log("info", f"Fluxo {flow_path.name} iniciado no perfil {metadata['name']}.")]
            if not steps:
                logs.append(self._log("warning", "Fluxo sem passos executaveis. Chrome persistente aberto."))
            for index, step in enumerate(steps, start=1):
                logs.append(await self._execute_step(page, step, index))

            title = await self._safe_title(page)
            self.last_execution = {
                "profile": metadata["name"],
                "flow": flow_path.name,
                "url": page.url,
                "title": title,
                "finished_at": self._timestamp(),
                "steps": len(steps),
            }
            logs.append(self._log("success", f"Fluxo finalizado em {page.url or 'about:blank'}."))

            return {
                "status": "success",
                "profile": metadata["name"],
                "flow": flow_path.name,
                "logs": logs,
                "active_browsers": self.active_browsers,
                "last_execution": self.last_execution,
            }

    async def run_actions(self, profile: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        async with self._lock:
            await self.start()
            context, page, metadata, profile_dir = await self._get_or_create_context(profile)
            metadata = self._touch_profile(profile_dir)
            logs = [self._log("info", f"Acao direta iniciada no perfil {metadata['name']}.")]
            for index, step in enumerate(steps, start=1):
                logs.append(await self._execute_step(page, step, index))

            self.last_execution = {
                "profile": metadata["name"],
                "flow": "acao-direta",
                "url": page.url,
                "title": await self._safe_title(page),
                "finished_at": self._timestamp(),
                "steps": len(steps),
            }
            return {
                "status": "success",
                "profile": metadata["name"],
                "flow": "acao-direta",
                "logs": logs,
                "active_browsers": self.active_browsers,
                "last_execution": self.last_execution,
            }

    async def status(self) -> dict[str, Any]:
        pages = []
        for page_id, page in list(self._pages.items()):
            if page.is_closed():
                continue
            profile_key = self._page_to_profile.get(page_id, page_id)
            profile_dir = self.profiles_dir / profile_key
            profile_name = profile_key
            if profile_dir.exists():
                profile_name = self._read_profile_metadata(profile_dir)["name"]
            
            title = ""
            try:
                # Try to get the page lock within a 1.0s timeout to get the safe title
                async with asyncio.timeout(1.0):
                    async with self.page_lock(page_id):
                        title = await self._safe_title(page)
            except Exception:
                title = ""

            pages.append(
                {
                    "id": page_id,
                    "profile": profile_name,
                    "url": page.url,
                    "title": title,
                }
            )
        return {
            "active_browsers": self.active_browsers,
            "last_execution": self.last_execution,
            "pages": pages,
        }

    @property
    def active_browsers(self) -> int:
        return len(self._contexts)

    def default_profile(self) -> str:
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("default"):
                return profile["name"]
        return profiles[0]["name"] if profiles else self.default_profile_name

    def _ensure_storage(self) -> None:
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.flows_dir.mkdir(parents=True, exist_ok=True)
        self._migrate_legacy_default_profile()

        profile_dirs = [path for path in self.profiles_dir.iterdir() if path.is_dir() and not path.name.startswith(".import-")]
        if not profile_dirs:
            default_dir = self.profiles_dir / self.sanitize_profile_dir_name(self.default_profile_name)
            default_dir.mkdir(parents=True, exist_ok=True)
            profile_dirs = [default_dir]

        for profile_dir in profile_dirs:
            self._ensure_profile_metadata(profile_dir)
        self._ensure_single_default()

    def _migrate_legacy_default_profile(self) -> None:
        legacy_dir = self.profiles_dir / self.default_profile_name
        target_dir = self.profiles_dir / self.sanitize_profile_dir_name(self.default_profile_name)
        if legacy_dir.exists() and legacy_dir.is_dir() and legacy_dir.resolve() != target_dir.resolve() and not target_dir.exists():
            legacy_dir.rename(target_dir)

    async def _get_or_create_context(self, profile: str) -> tuple[BrowserContext, Page, dict[str, Any], Path]:
        profile_dir = self._find_profile_dir(profile)
        metadata = self._read_profile_metadata(profile_dir)
        profile_key = profile_dir.name
        context = self._contexts.get(profile_key)

        if context is None:
            if self._playwright is None:
                raise BrowserRunError("Playwright nao foi iniciado.")
            context = await self._playwright.chromium.launch_persistent_context(
                user_data_dir=str(profile_dir),
                channel="chrome",
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--restore-last-session"
                ],
                ignore_default_args=["--enable-automation"],
                no_viewport=True,
            )
            await context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            )
            context.set_default_timeout(30_000)
            context.on("close", lambda *_: self._forget_context(profile_key))
            self._contexts[profile_key] = context
        
        for i, p in enumerate(context.pages):
            print(i, p.url)
        page = self._pages.get(profile_key)
        if page is None or page.is_closed():
            # Dá tempo para o Chrome restaurar a sessão
            for _ in range(20):          # espera até 2 segundos
                if context.pages:
                    break
                await asyncio.sleep(0.1)

            if context.pages:
                page = context.pages[-1]
            else:
                page = await context.new_page()
            
            for p in list(context.pages):
                if p.url == "about:blank" and len(context.pages) > 1:
                    await p.close()
        
        for i, p in enumerate(context.pages):
            print(i, p.url)
        self.register_page(profile_key, page, profile_key)
        return context, page, metadata, profile_dir

    def _forget_context(self, profile_key: str) -> None:
        self._contexts.pop(profile_key, None)
        self._pages.pop(profile_key, None)

    async def _close_profile_context(self, profile_dir: Path) -> None:
        profile_key = profile_dir.name
        context = self._contexts.pop(profile_key, None)
        self._pages.pop(profile_key, None)
        if context is not None:
            await context.close()

    def _resolve_profile_dir(self, profile: str) -> Path:
        return self._find_profile_dir(profile)

    def _find_profile_dir(self, profile: str) -> Path:
        self._ensure_storage_shallow()
        profile_name = self._clean_profile_name(profile)
        candidates = [
            self.profiles_dir / self.sanitize_profile_dir_name(profile_name),
            self.profiles_dir / profile_name,
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_dir():
                return candidate

        for profile_dir in self.profiles_dir.iterdir():
            if not profile_dir.is_dir() or profile_dir.name.startswith(".import-"):
                continue
            metadata = self._read_profile_metadata(profile_dir)
            if metadata["name"].casefold() == profile_name.casefold():
                return profile_dir
        raise FileNotFoundError(f"Perfil nao encontrado: {profile_name}")

    def _ensure_storage_shallow(self) -> None:
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.flows_dir.mkdir(parents=True, exist_ok=True)

    def _profile_name_exists(self, profile_name: str) -> bool:
        if not self.profiles_dir.exists():
            return False
        wanted = self._clean_profile_name(profile_name).casefold()
        wanted_dir = self.sanitize_profile_dir_name(profile_name).casefold()
        for profile_dir in self.profiles_dir.iterdir():
            if not profile_dir.is_dir() or profile_dir.name.startswith(".import-"):
                continue
            if profile_dir.name.casefold() == wanted_dir:
                return True
            metadata = self._read_profile_metadata(profile_dir)
            if metadata["name"].casefold() == wanted:
                return True
        return False

    def _ensure_profile_metadata(self, profile_dir: Path) -> dict[str, Any]:
        metadata_path = profile_dir / "profile.json"
        if metadata_path.exists():
            try:
                raw = json.loads(metadata_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise BrowserRunError(f"profile.json invalido em {profile_dir.name}: {exc}") from exc
        else:
            raw = {}

        metadata = {
            "name": self._clean_profile_name(raw.get("name") or self._display_name_from_dir(profile_dir.name)),
            "created_at": str(raw.get("created_at") or self._iso_timestamp()),
            "last_used": raw.get("last_used"),
            "default": bool(raw.get("default", False)),
        }
        self._write_profile_metadata(profile_dir, metadata)
        return metadata

    def _read_profile_metadata(self, profile_dir: Path) -> dict[str, Any]:
        return self._ensure_profile_metadata(profile_dir)

    def _write_profile_metadata(self, profile_dir: Path, metadata: dict[str, Any]) -> None:
        profile_dir.mkdir(parents=True, exist_ok=True)
        normalized = {
            "name": self._clean_profile_name(metadata.get("name")),
            "created_at": str(metadata.get("created_at") or self._iso_timestamp()),
            "last_used": metadata.get("last_used"),
            "default": bool(metadata.get("default", False)),
        }
        (profile_dir / "profile.json").write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    def _touch_profile(self, profile_dir: Path) -> dict[str, Any]:
        metadata = self._read_profile_metadata(profile_dir)
        metadata["last_used"] = self._iso_timestamp()
        self._write_profile_metadata(profile_dir, metadata)
        return metadata

    def _ensure_single_default(self) -> None:
        profile_dirs = [path for path in sorted(self.profiles_dir.iterdir(), key=lambda item: item.name.lower()) if path.is_dir() and not path.name.startswith(".import-")]
        if not profile_dirs:
            return

        default_seen = False
        for profile_dir in profile_dirs:
            metadata = self._read_profile_metadata(profile_dir)
            if metadata.get("default") and not default_seen:
                default_seen = True
                continue
            if metadata.get("default"):
                metadata["default"] = False
                self._write_profile_metadata(profile_dir, metadata)

        if not default_seen:
            metadata = self._read_profile_metadata(profile_dirs[0])
            metadata["default"] = True
            self._write_profile_metadata(profile_dirs[0], metadata)

    def _set_only_default(self, selected_dir: Path) -> dict[str, Any]:
        selected_dir = selected_dir.resolve()
        selected_metadata: dict[str, Any] | None = None
        for profile_dir in self.profiles_dir.iterdir():
            if not profile_dir.is_dir() or profile_dir.name.startswith(".import-"):
                continue
            metadata = self._read_profile_metadata(profile_dir)
            metadata["default"] = profile_dir.resolve() == selected_dir
            self._write_profile_metadata(profile_dir, metadata)
            if metadata["default"]:
                selected_metadata = metadata
        if selected_metadata is None:
            raise FileNotFoundError("Perfil padrao nao encontrado.")
        return selected_metadata

    def sanitize_profile_dir_name(self, name: str) -> str:
        display_name = self._clean_profile_name(name)
        chars = []
        for char in display_name:
            if char.isspace():
                chars.append("_")
            elif char.isalnum() or char in "-_.":
                chars.append(char)
            else:
                chars.append("_")
        safe = re.sub(r"_+", "_", "".join(chars)).strip("._ ")
        if not safe:
            raise ValueError("Nome de perfil invalido.")
        return safe[:120]

    def _clean_profile_name(self, name: Any) -> str:
        cleaned = " ".join(str(name or "").strip().split())
        if not cleaned:
            raise ValueError("Nome de perfil obrigatorio.")
        if cleaned in {".", ".."} or "/" in cleaned or "\\" in cleaned:
            raise ValueError("Nome de perfil invalido.")
        return cleaned[:120]

    def _display_name_from_dir(self, dir_name: str) -> str:
        return " ".join(dir_name.replace("_", " ").split()) or self.default_profile_name

    def _safe_rmtree(self, target_dir
    : Path) -> None:
        target = target_dir.resolve()
        root = self.profiles_dir.resolve()
        self._assert_child_path(root, target)
        if target == root:
            raise ValueError("Nao e permitido remover a pasta profiles.")
        shutil.rmtree(target)

    def _assert_child_path(self, root: Path, child: Path) -> None:
        root_resolved = root.resolve()
        child_resolved = child.resolve()
        if root_resolved != child_resolved and root_resolved not in child_resolved.parents:
            raise ValueError("Caminho fora da pasta de perfis.")

    def _validate_zip_members(self, members: list[zipfile.ZipInfo]) -> None:
        for member in members:
            path = PurePosixPath(member.filename)
            if path.is_absolute() or ".." in path.parts:
                raise BrowserRunError("ZIP contem caminho inseguro.")

    def _find_profile_json_member(self, members: list[zipfile.ZipInfo]) -> str:
        candidates = [member.filename for member in members if not member.is_dir() and PurePosixPath(member.filename).name == "profile.json"]
        if not candidates:
            raise BrowserRunError("ZIP nao contem profile.json.")
        return sorted(candidates, key=lambda item: len(PurePosixPath(item).parts))[0]

    def _load_imported_metadata(self, content: bytes) -> dict[str, Any]:
        try:
            raw = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BrowserRunError("profile.json importado e invalido.") from exc
        missing = [field for field in ("name", "created_at", "last_used", "default") if field not in raw]
        if missing:
            raise BrowserRunError(f"profile.json sem campos obrigatorios: {', '.join(missing)}")
        return {
            "name": self._clean_profile_name(raw["name"]),
            "created_at": str(raw["created_at"]),
            "last_used": raw.get("last_used"),
            "default": bool(raw.get("default", False)),
        }

    def _resolve_flow_path(self, flow: str) -> Path:
        flow_name = self.safe_flow_filename(flow)
        if not flow_name.endswith(".json"):
            flow_name += ".json"
        
        flow_path = self.flows_dir / flow_name
        if not flow_path.exists() or not flow_path.is_file():
            raise FileNotFoundError(f"Fluxo nao encontrado: {flow_name}")
        return flow_path

    def safe_flow_filename(self, flow: str) -> str:
        value = self._safe_segment(flow, "fluxo")
        if not value.lower().endswith(".json"):
            value = f"{value}.json"
        if Path(value).name != value:
            raise ValueError("Nome do fluxo nao pode conter diretorios.")
        return value

    def _safe_segment(self, value: str, label: str) -> str:
        cleaned = str(value).strip()
        if not cleaned:
            raise ValueError(f"Nome de {label} obrigatorio.")
        if cleaned in {".", ".."} or "/" in cleaned or "\\" in cleaned:
            raise ValueError(f"Nome de {label} invalido.")
        return cleaned

    def _load_flow(self, flow_path: Path) -> Any:
        try:
            return json.loads(flow_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise BrowserRunError(f"JSON invalido em {flow_path.name}: {exc}") from exc

    async def _execute_flow_step(self, page: Page, flow_name: str, index: int) -> dict[str, str]:
        flow_path = self._resolve_flow_path(flow_name)
        flow_data = self._load_flow(flow_path)
        steps = self._extract_steps(flow_data)

        if not steps:
            return self._log("info", f"Passo {index}: fluxo {flow_path.name} sem passos.")

        for sub_idx, sub_step in enumerate(steps, start=1):
            await self._execute_step(page, sub_step, f"{index}.{sub_idx}")

        return self._log("success", f"Passo {index}: fluxo {flow_path.name} executado.")

    def _extract_steps(self, flow_data: Any) -> list[dict[str, Any]]:
        if isinstance(flow_data, list):
            return [step for step in flow_data if isinstance(step, dict)]
        if not isinstance(flow_data, dict):
            raise BrowserRunError("Fluxo deve ser um objeto JSON ou uma lista de passos.")
        if isinstance(flow_data.get("steps"), list):
            return [step for step in flow_data["steps"] if isinstance(step, dict)]
        if isinstance(flow_data.get("actions"), list):
            return [step for step in flow_data["actions"] if isinstance(step, dict)]
        if flow_data.get("url"):
            return [{"action": "navigate", "url": flow_data["url"]}]
        return []

    async def _execute_step(self, page: Page, step: dict[str, Any], index: int) -> dict[str, str]:
        page_id = self.get_page_id(page)
        if page_id:
            async with self.page_lock(page_id):
                return await self._execute_step_inner(page, step, index)
        else:
            return await self._execute_step_inner(page, step, index)

    async def _execute_step_inner(self, page: Page, step: dict[str, Any], index: int) -> dict[str, str]:
        action = str(step.get("action") or step.get("type") or step.get("acao") or "").strip().lower()
        if not action:
            raise BrowserRunError(f"Passo {index} sem action.")

        if action in {"navigate", "goto", "navegar"}:
            url = self._resolve_variables(self._required(step, "url", index))
            await page.goto(url, wait_until=str(step.get("wait_until") or "domcontentloaded"))
            return self._log("success", f"Passo {index}: navegou para {url}.")

        if action in {"fill", "preencher"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            value = self._resolve_variables(str(step.get("value", step.get("valor", ""))))
            await page.fill(selector, value)
            return self._log("success", f"Passo {index}: preencheu {selector}.")

        if action in {"click", "clicar"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            await page.click(selector)
            return self._log("success", f"Passo {index}: clicou em {selector}.")

        if action in {"press", "tecla"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            key = self._required(step, "key", index, fallback="tecla")
            await page.press(selector, key)
            return self._log("success", f"Passo {index}: pressionou {key}.")

        if action in {"wait", "aguardar"}:
            seconds = float(step.get("seconds", step.get("segundos", 1)))
            await asyncio.sleep(seconds)
            return self._log("info", f"Passo {index}: aguardou {seconds:g}s.")
        
        if action in {"monitor", "monitorar"}:
            selector = step.get("selector", step.get("seletor"))
            if not selector:
                raise BrowserRunError(f"Passo {index} (monitor) sem selector.")
            
            page_id = self.get_page_id(page)
            if not page_id:
                raise BrowserRunError(f"Passo {index}: Página não registrada.")
            profile = self._page_to_profile.get(page_id, page_id)
            
            monitor_name = step.get("name", step.get("nome", f"Monitor {selector}"))
            monitor_type = step.get("type", "DOM")
            attribute = step.get("attribute", step.get("atributo", "textcontent"))
            interval = float(step.get("interval", step.get("intervalo", 10.0)))
            timeout = float(step.get("timeout", 30.0))
            save_snapshots = self._normalize_value(step.get("save_snapshots", step.get("save", False)))
            max_history = int(step.get("max_history", 100))
            on_change_steps = step.get("on_change", [])
            on_not_found_steps = step.get("on_not_found", [])
            
            from app.monitor.manager import monitor_manager
            
            monitor = await monitor_manager.register_monitor(
                name=monitor_name,
                type=monitor_type,
                profile=profile,
                page_id=page_id,
                frame_id=step.get("frame_id"),
                selector=selector,
                attribute=attribute,
                interval=interval,
                timeout=timeout,
                save_snapshots=save_snapshots,
                max_history=max_history,
                on_change=on_change_steps,
                on_not_found=on_not_found_steps

            )
            
            await monitor_manager.start_monitor(monitor.id)
            
            return self._log(
                "success",
                f"Passo {index}: Monitor '{monitor.name}' (ID: {monitor.id}) registrado e iniciado em background."
            )

        if action in {"wait_for_selector", "aguardar_seletor"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            timeout = step.get("timeout", 30000)  # padrão 30 segundos

            # Nome da variável para armazenar o resultado (padrão: SELETOR)
            var_name = step.get("var", "SELETOR")

            try:
                await page.wait_for_selector(selector, timeout=timeout)
                # Seletor encontrado → armazena True na variável
                self._variables[var_name] = True
                self._log(
                    "info",
                    f"Passo {index}: seletor '{selector}' encontrado. Variável {var_name} = True"
                )
                return self._log("success", f"Passo {index}: encontrou {selector}.")
            except TimeoutError:
                # Seletor NÃO encontrado → armazena False
                self._variables[var_name] = False
                self._log(
                    "info",
                    f"Passo {index}: seletor '{selector}' NÃO encontrado (timeout). Variável {var_name} = False"
                )
                return self._log("success", f"Passo {index}: seletor não encontrado, mas fluxo continua.")

        if action in {"flow", "fluxo"}:
            flow_name = self._resolve_variables(
                self._required(step, "flow", index, fallback="flow_name")
            )
            return await self._execute_flow_step(page, flow_name, index)
                
        if action in {"screenshot", "capturar"}:
            filename = step.get("filename", step.get("arquivo", f"screenshot_{index}.png"))
            # Cria o diretório se não existir
            from pathlib import Path
            path = Path(filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(path))
            return self._log("success", f"Passo {index}: screenshot salvo em {filename}.")

        if action in {"extract", "extrair"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            var_name = self._required(step, "variable", index, fallback="variavel")

            # padrão: extrai tudo
            attr = step.get("attribute", step.get("atributo", "all"))
            multiple = step.get("multiple", False)

            async def extract_element(el):
                if not el:
                    return None

                if attr.lower() == "all":
                    return await el.evaluate("""
                    (e) => ({
                        text: e.textContent?.trim(),
                        innerText: e.innerText?.trim(),
                        html: e.innerHTML,
                        outerHtml: e.outerHTML,
                        value: e.value || null,
                        href: e.href || null,
                        src: e.src || null,
                        id: e.id || null,
                        class: e.className || null,
                        name: e.name || null,
                        dataset: {...e.dataset},
                        attributes: Object.fromEntries(
                            [...e.attributes].map(a => [a.name, a.value])
                        )
                    })
                    """)

                elif attr.lower() == "textcontent":
                    return (await el.text_content() or "").strip()

                elif attr.lower() == "innertext":
                    return (await el.inner_text() or "").strip()

                elif attr.lower() in {"html", "innerhtml"}:
                    return await el.inner_html()

                elif attr.lower() == "outerhtml":
                    return await el.evaluate("(e)=>e.outerHTML")

                else:
                    return await el.get_attribute(attr)

            # múltiplos elementos
            if multiple:
                elements = await page.query_selector_all(selector)
                value = []

                for el in elements:
                    result = await extract_element(el)
                    value.append(result)

            else:
                element = await page.query_selector(selector)
                value = await extract_element(element)

            # salva variável
            if not hasattr(self, "_variables"):
                self._variables = {}

            self._variables[var_name] = value

            return self._log(
                "success",
                f"Passo {index}: extraiu {var_name}"
            )

        if action in {"extracthtml","extrairhtml"}:

            source = self._required(step, "source", index)

            selector = self._required(step, "selector", index)

            var_name = self._required(step, "variable", index)

            attr = step.get(
                "attribute",
                "textContent"
            )

            html = self._variables.get(source)

            if not html:

                return self._log(
                    "error",
                    f"HTML '{source}' não encontrado."
                )

            value = await page.evaluate(
                """
                ({html, selector, attr}) => {

                    const parser = new DOMParser();

                    const doc = parser.parseFromString(
                        html,
                        "text/html"
                    );

                    const el = doc.querySelector(selector);

                    if (!el)
                        return null;

                    const attrLower = attr.toLowerCase();

                    if (attrLower === "textcontent")
                        return el.textContent?.trim();

                    if (attrLower === "innertext")
                        return el.innerText?.trim();

                    if (
                        attrLower === "html" ||
                        attrLower === "innerhtml"
                    )
                        return el.innerHTML;

                    if (
                        attrLower === "outer" ||
                        attrLower === "outerhtml"
                    )
                        return el.outerHTML;

                    return el.getAttribute(attr);
                }
                """,
                {
                    "html": html,
                    "selector": selector,
                    "attr": attr
                }
            )

            self._variables[var_name] = value

        if action in {"select", "selecionar"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            value = self._resolve_variables(self._required(step, "value", index, fallback="valor"))
            await page.select_option(selector, value)
            return self._log("success", f"Passo {index}: selecionou {value} em {selector}.")

        if action in {"hover", "pairar"}:
            selector = self._required(step, "selector", index, fallback="seletor")
            await page.hover(selector)
            return self._log("success", f"Passo {index}: pairou sobre {selector}.")    
        
        if action in {"log", "registrar"}:
            message = step.get("message", step.get("mensagem", ""))

            if hasattr(self, "_variables"):
                message = message.format_map(
                    SafeDict(self._variables)
                )

            return self._log("info", message)
        
        if action in {"loop","repetir"}:
            times = step.get("times", 1)  # número de iterações, None para infinito
            interval = step.get("interval", 0)  # segundos entre iterações
            sub_steps = step.get("steps", [])
            if not sub_steps:
                raise BrowserRunError(f"Passo {index}: loop sem steps.")

             # Variáveis de controle
            iteration = 0
            while times is None or iteration < times:
                self._variables["_loop_iteration"] = iteration
                self._variables["_loop_total"] = times

                for sub_idx, sub_step in enumerate(sub_steps):
                    # Executa cada sub-passo com índice composto
                    await self._execute_step(page, sub_step, f"{index}.{sub_idx}")

                iteration += 1
                if interval > 0 and (times is None or iteration < times):
                    await asyncio.sleep(interval)
            return self._log("success", f"Loop executado {iteration} vezes.")

        if action == "set":
            var_name = self._required(step, "var", index)

            value = self._resolve_variables(
                step.get("value", "")
            )
            value = self._normalize_value(value)

            self._variables[var_name] = value

            return self._log(
                "info",
                f"Variável {var_name} = {value}"
            )

        if action in {"compare", "comparar"}:

            if not hasattr(self, "_variables"):
                self._variables = {}

            def _as_list(value):
                if value is None:
                    return []
                if isinstance(value, list):
                    return value
                return [value]

            var_name = self._required(step, "var", index)

            operator = str(step.get("operator", "==")).lower()

            expected = self._normalize_value(self._resolve_variables(step.get("value", "")))
            current = self._normalize_value(self._variables.get(var_name))

            def _to_number(value):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return None

            current_number = _to_number(current)
            expected_number = _to_number(expected)

            def _to_string(value):
                if value is None:
                    return ""
                if isinstance(value, bool):
                    return "true" if value else "false"
                return str(value)

            current_str = _to_string(current)
            expected_str = _to_string(expected)

            condition_met = False

            if operator == "==":
                condition_met = current_str == expected_str

            elif operator == "!=":
                condition_met = current_str != expected_str

            elif operator == ">":
                if current_number is not None and expected_number is not None:
                    condition_met = current_number > expected_number

            elif operator == "<":
                if current_number is not None and expected_number is not None:
                    condition_met = current_number < expected_number

            elif operator == ">=":
                if current_number is not None and expected_number is not None:
                    condition_met = current_number >= expected_number

            elif operator == "<=":
                if current_number is not None and expected_number is not None:
                    condition_met = current_number <= expected_number

            elif operator == "contains":
                condition_met = expected_str in current_str

            elif operator == "not_contains":
                condition_met = expected_str not in current_str

            elif operator == "startswith":
                condition_met = current_str.startswith(expected_str)

            elif operator == "endswith":
                condition_met = current_str.endswith(expected_str)

            else:
                raise BrowserRunError(
                    f"Operador inválido: {operator}"
                )

            target_steps = _as_list(
                step.get(
                    "on_true" if condition_met else "on_false"
                )
            )
            print("Executando branch:", target_steps)

            for sub_idx, sub_step in enumerate(target_steps):
                print("Substep:", sub_step)
                await self._execute_step(
                    page,
                    sub_step,
                    f"{index}.{sub_idx}"
                )

            return self._log(
                "success",
                (
                    f"Passo {index}: comparação "
                    f"{var_name} {operator} {expected_str} "
                    f"-> {condition_met}"
                )
            )

        if action == "notify":
            webhook_url = step.get("webhook")
            payload = step.get("payload", {})
            # Substitui placeholders no payload
            if isinstance(payload, dict):
                payload = self._resolve_variables(step.get("payload", {}))
            if webhook_url:
                import requests
                response = requests.post(webhook_url, json=payload, timeout=5)
                return self._log("info", f"Notificação enviada: {response.status_code}")
            else:
                # Fallback para log
                return self._log("info", f"Notificação: {payload}")
            

        raise BrowserRunError(f"Acao nao suportada no passo {index}: {action}")

    def _required(self, step: dict[str, Any], key: str, index: int, fallback: str | None = None) -> str:
        value = step.get(key)
        if value is None and fallback is not None:
            value = step.get(fallback)
        if value is None or str(value).strip() == "":
            raise BrowserRunError(f"Passo {index} sem campo obrigatorio: {key}.")
        return str(value)

    async def _safe_title(self, page: Page) -> str:
        try:
            return await page.title()
        except Exception:
            return ""

    def _log(self, tipo: str, mensagem: str) -> dict[str, str]:
        return {"timestamp": self._timestamp(), "tipo": tipo, "mensagem": mensagem}

    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _iso_timestamp(self) -> str:
        return datetime.now().replace(microsecond=0).isoformat()


