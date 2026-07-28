import asyncio
import traceback
from datetime import datetime
from typing import Any
from app.monitor.types import MonitorStatus
from app.monitor.diff import normalize_content, generate_diff
from bs4 import BeautifulSoup, NavigableString, Tag


TAGS = {
    "button": "Botão",
    "a": "Link",
    "input": "Campo",
    "textarea": "Área de texto",
    "select": "Lista de seleção",
    "option": "Opção",
    "img": "Imagem",
    "svg": "Ícone",
    "form": "Formulário",
    "table": "Tabela",
    "tr": "Linha",
    "td": "Coluna",
    "th": "Cabeçalho",
    "ul": "Lista",
    "ol": "Lista ordenada",
    "li": "Item",
    "label": "Rótulo",
    "video": "Vídeo",
    "audio": "Áudio",
}


def dom_para_texto(html: str) -> str:
    """
    Converte um trecho HTML em uma descrição simples em português.

    Ignora:
    - classes
    - estilos
    - ids
    - atributos visuais

    Mantém:
    - tipo do elemento
    - textos
    - atributos úteis (href, src, placeholder, value, title...)
    """

    soup = BeautifulSoup(html, "html.parser")

    linhas = []

    def texto_direto(tag: Tag) -> str:
        textos = []

        for child in tag.children:
            if isinstance(child, NavigableString):
                t = child.strip()
                if t:
                    textos.append(t)

        return " ".join(textos)

    def visitar(node: Tag, nivel=0):

        if not isinstance(node, Tag):
            return

        nome = TAGS.get(node.name)

        if nome:

            atributos = []

            if node.name == "input":
                tipo = node.get("type", "text")
                atributos.append(f"tipo={tipo}")

            for attr in (
                "placeholder",
                "value",
                "title",
                "alt",
                "href",
                "src",
                "name",
            ):
                valor = node.get(attr)
                if valor:
                    atributos.append(f'{attr}="{valor}"')

            texto = texto_direto(node)

            linha = "  " * nivel + f"- {nome}"

            if atributos:
                linha += " (" + ", ".join(atributos) + ")"

            if texto:
                linha += f': "{texto}"'

            linhas.append(linha)

            nivel += 1

        elif node.name not in (
            "div",
            "span",
            "section",
            "article",
            "main",
            "header",
            "footer",
            "nav",
        ):
            linhas.append("  " * nivel + f"- {node.name}")
            nivel += 1

        for child in node.children:
            if isinstance(child, Tag):
                visitar(child, nivel)

        # Texto que ficou solto
        for child in node.children:
            if isinstance(child, NavigableString):
                t = child.strip()
                if t:
                    linhas.append("  " * nivel + f'• Texto: "{t}"')

    for child in soup.children:
        if isinstance(child, Tag):
            visitar(child)

    if not linhas:
        return "Nenhum elemento relevante encontrado."

    return "\n".join(linhas)


class ElementNotFoundError(Exception):
    """Internal exception for element not found scenarios."""
    pass

async def monitor_worker(monitor_id: str, manager: Any) -> None:
    """
    Main worker loop for a single monitor.
    Runs continuously as long as monitor.status == MonitorStatus.RUNNING.
    """
    # Use delayed imports to avoid circular dependencies
    browser_manager = manager.browser_manager
    storage = manager.storage

    while True:
        # Re-fetch monitor configuration to check status
        monitor = manager.get_monitor(monitor_id)
        if not monitor or (monitor.status not in {MonitorStatus.RUNNING, MonitorStatus.NOT_FOUND}):
            break

        # 1. Aguardar intervalo (sleep first as specified by the flow)
        try:
            await asyncio.sleep(monitor.interval)
        except asyncio.CancelledError:
            break

        # Re-fetch monitor config after sleep
        monitor = manager.get_monitor(monitor_id)
        if not monitor or (monitor.status not in {MonitorStatus.RUNNING, MonitorStatus.NOT_FOUND}):
            break

        page_id = monitor.page_id
        lock_acquired = False

        try:
            # 2. Adquirir lock
            await browser_manager.acquire_lock(page_id)
            lock_acquired = True

            # 3. Obter página através do BrowserManager e verificar existência
            if not browser_manager.is_page_alive(page_id):
                monitor.status = MonitorStatus.ERROR
                monitor.last_error = "Página encerrada ou indisponível."
                storage.save_current(monitor)
                break

            page = browser_manager.get_page(page_id)
            if not page:
                monitor.status = MonitorStatus.ERROR
                monitor.last_error = "Página não encontrada no BrowserManager."
                storage.save_current(monitor)
                break

            # If frame_id is specified, locate frame
            target = page
            if monitor.frame_id:
                frame = browser_manager.get_frame(monitor.frame_id)
                if not frame:
                    monitor.status = MonitorStatus.ERROR
                    monitor.last_error = f"Frame '{monitor.frame_id}' não encontrado."
                    storage.save_current(monitor)
                    break
                target = frame

            # 4. Localizar elemento e extrair atributo
            # Use a quick timeout for locating elements to avoid infinite hanging
            locator = target.locator(monitor.selector)
            
            try:
                # Wait for element presence with monitor timeout (e.g. 5 seconds default or configured)
                await locator.first.wait_for(state="attached", timeout=min(5000, int(monitor.timeout * 1000)))
            except Exception:
                raise ElementNotFoundError(f"Elemento com seletor '{monitor.selector}' não foi anexado ao DOM.")

            count = await locator.count()
            if count == 0:
                raise ElementNotFoundError(f"Elemento com seletor '{monitor.selector}' não encontrado.")

            # Restore status to RUNNING if it was in NOT_FOUND
            if monitor.status == MonitorStatus.NOT_FOUND:
                monitor.status = MonitorStatus.RUNNING

            element = locator.first
            attr = str(monitor.attribute).lower()

            if attr == "textcontent":
                value = await element.text_content()
            elif attr == "innertext":
                value = await element.inner_text()
            elif attr in {"html", "innerhtml"}:
                value = await element.inner_html()
            elif attr == "outerhtml":
                value = await element.evaluate("e => e.outerHTML")
            else:
                value = await element.get_attribute(monitor.attribute)

            value_str = (value or "").strip()

            # 5. Normalizar conteúdo
            norm_value = normalize_content(value_str, monitor.attribute)

            # 6. Comparar
            old_norm = normalize_content(monitor.last_value or "", monitor.attribute)

            monitor.verification_count += 1
            monitor.last_check = datetime.now().replace(microsecond=0).isoformat()

            # If first run or value changes
            if monitor.last_value is None or norm_value != old_norm:
                # 7. Gerar diff
                diff_text = generate_diff(old_norm, norm_value) if monitor.last_value is not None else ""
                
                
                # Update change tracking
                monitor.changes_count += 1
                monitor.last_change = monitor.last_check
                monitor.last_value = value_str

                # Salvar no contexto do monitor
                monitor.context["last_diff"] = dom_para_texto(diff_text)
                monitor.context["previous_value"] = dom_para_texto(old_norm)
                monitor.context["current_value"] = dom_para_texto(norm_value)

                # 8. Snapshots (Salvar snapshots apenas quando save_snapshots == True)
                snapshot_file = None
                if monitor.save_snapshots:
                    try:
                        file_name = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        screenshot_bytes = await page.screenshot(type="png")
                        storage.save_snapshot(monitor.id, file_name, screenshot_bytes)
                        snapshot_file = file_name
                    except Exception as se:
                        print(f"Erro ao capturar snapshot: {se}")

                # 9. Persistir dados (append history)
                history_entry = {
                    "timestamp": monitor.last_check,
                    "status": monitor.status,
                    "value": dom_para_texto(value_str),
                    "diff": dom_para_texto(diff_text) if monitor.last_value is not None else None,
                    "snapshot": snapshot_file,
                    "error": None
                }
                storage.append_history(monitor.id, history_entry, monitor.max_history)

                # 10. Disparar on_change (async task in background)
                if monitor.on_change:
                    manager.trigger_on_change(monitor.id, monitor.on_change)
            else:
                # No change, but let's record verification and save
                pass

            monitor.last_error = None

        except ElementNotFoundError as e:
            # Element not found: treat as NOT_FOUND event (not as an error)
            error_msg = str(e)
            monitor.last_error = error_msg
            monitor.last_check = datetime.now().replace(microsecond=0).isoformat()
            
            # Set status to NOT_FOUND (visual indicator)
            monitor.status = MonitorStatus.NOT_FOUND
            
            # Append to history with event marker
            history_entry = {
                "timestamp": monitor.last_check,
                "status": monitor.status,
                "value": monitor.last_value,
                "diff": None,
                "snapshot": None,
                "error": error_msg,
                "event": "NOT_FOUND"
            }
            storage.append_history(monitor.id, history_entry, monitor.max_history)
            
            # Trigger on_not_found if steps are configured
            if monitor.on_not_found:
                manager.trigger_on_not_found(monitor.id, monitor.on_not_found)

        except Exception as e:
            error_msg = str(e)
            monitor.last_error = error_msg
            monitor.last_check = datetime.now().replace(microsecond=0).isoformat()

            # Append error to history
            history_entry = {
                "timestamp": monitor.last_check,
                "status": monitor.status,
                "value": monitor.last_value,
                "diff": None,
                "snapshot": None,
                "error": error_msg
            }
            storage.append_history(monitor.id, history_entry, monitor.max_history)

        finally:
            # 11. Liberar lock
            if lock_acquired:
                browser_manager.release_lock(page_id)
            
            # Always save current state
            storage.save_current(monitor)


async def run_on_change(monitor_id: str, steps: list[dict[str, Any]], manager: Any) -> None:
    """
    Executes the on_change automation flow in an independent task.
    """
    monitor = manager.get_monitor(monitor_id)
    if not monitor:
        return

    page_id = monitor.page_id
    browser_manager = manager.browser_manager
    storage = manager.storage

    lock_acquired = False
    try:
        # Acquire page lock
        await browser_manager.acquire_lock(page_id)
        lock_acquired = True

        page = browser_manager.get_page(page_id)
        if not page or page.is_closed():
            raise ValueError("Página associada indisponível para executar fluxo on_change.")

        # Bind the monitor's private context variables dictionary
        browser_manager._variables_var.set(monitor.context)

        # Run each action step sequentially
        for index, step in enumerate(steps, start=1):
            await browser_manager._execute_step(page, step, f"on_change_{index}")

    except Exception as e:
        print(f"Erro ao executar on_change para monitor {monitor_id}: {e}")
        traceback.print_exc()
        monitor.last_error = f"Erro no on_change: {e}"
        storage.save_current(monitor)
    finally:
        if lock_acquired:
            browser_manager.release_lock(page_id)


async def run_on_not_found(monitor_id: str, steps: list[dict[str, Any]], manager: Any) -> None:
    """
    Executes the on_not_found automation flow in an independent task.
    """
    # print(f"Executando fluxo on_not_found para monitor {monitor_id} com {len(steps)} etapas.")
    monitor = manager.get_monitor(monitor_id)
    if not monitor:
        return

    page_id = monitor.page_id
    browser_manager = manager.browser_manager
    storage = manager.storage

    lock_acquired = False
    try:
        # Acquire page lock
        await browser_manager.acquire_lock(page_id)
        lock_acquired = True

        page = browser_manager.get_page(page_id)
        if not page or page.is_closed():
            raise ValueError("Página associada indisponível para executar fluxo on_not_found.")

        # Bind the monitor's private context variables dictionary
        browser_manager._variables_var.set(monitor.context)

        # Run each action step sequentially
        for index, step in enumerate(steps, start=1):
            await browser_manager._execute_step(page, step, f"on_not_found_{index}")

    except Exception as e:
        print(f"Erro ao executar on_not_found para monitor {monitor_id}: {e}")
        traceback.print_exc()
        monitor.last_error = f"Erro no on_not_found: {e}"
        storage.save_current(monitor)
    finally:
        if lock_acquired:
            browser_manager.release_lock(page_id)
