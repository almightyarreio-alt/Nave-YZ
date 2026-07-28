import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app.core.browser import BrowserManager, BrowserRunError
from app.monitor.manager import MonitorManager
from app.models.schemas import (
    ActionClick,
    ActionFill,
    ActionNavigate,
    FlowSavedResponse,
    FlowSaveRequest,
    ProfileCreateRequest,
    ProfileDefaultRequest,
    ProfileMetadata,
    ProfileOpenRequest,
    ProfileOperationResponse,
    ProfileRenameRequest,
    RunFlowRequest,
    RunFlowResponse,
)
from notificacoes.config import carregar_configuracao, salvar_configuracao
from notificacoes.dispatcher import registrarEvento
from notificacoes.evento import EventoNotificacao
from notificacoes.receiver import (
    carregar_historico,
    montar_url_recepcao,
    payload_para_evento,
    registrar_webhook_recebido,
)

router = APIRouter()

PASTA_SONS = Path("sons")


EVENTO_TESTE_NOTIFICACAO = EventoNotificacao(
    tipo="info",
    titulo="Fluxo Finalizado",
    mensagem="Fluxo executado com sucesso.",
)


def _base_dir(request: Request) -> Path:
    return request.app.state.base_dir


def _manager(request: Request) -> BrowserManager:
    return request.app.state.browser_manager


def _model_dump(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _profile_error(exc: Exception) -> HTTPException:
    if isinstance(exc, FileNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, FileExistsError):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, (ValueError, BrowserRunError)):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=500, detail=f"Falha na operacao de perfil: {exc}")


def _testar_canal_notificacao(nome_canal: str) -> dict[str, Any]:
    configuracao_original = carregar_configuracao()
    configuracao_teste = json.loads(json.dumps(configuracao_original))

    configuracao_teste.setdefault("notifications", {})["enabled"] = True
    for canal in ("toast", "sound", "webhook"):
        configuracao_teste.setdefault(canal, {})["enabled"] = canal == nome_canal

    salvar_configuracao(configuracao_teste)
    try:
        return registrarEvento(EVENTO_TESTE_NOTIFICACAO)
    finally:
        salvar_configuracao(configuracao_original)


@router.post("/config/notificacoes/upload-audio")
async def upload_audio(
    arquivo: UploadFile = File(...)
):
    extensoes_permitidas = [".wav",".mp3"]

    extensao = Path(arquivo.filename).suffix.lower()

    if extensao not in extensoes_permitidas:
        raise HTTPException(
            status_code=400,
            detail="Formato de áudio não permitido"
        )

    PASTA_SONS.mkdir(exist_ok=True)
    destino = PASTA_SONS / arquivo.filename
    conteudo = await arquivo.read()

    destino.write_bytes(conteudo)

    return {
        "mensagem": "Áudio salvo",
        "file": arquivo.filename
    }


@router.get("/config/notificacoes")
async def obter_configuracao_notificacoes() -> dict[str, Any]:
    return carregar_configuracao()


@router.post("/config/notificacoes")
async def salvar_configuracao_notificacoes(configuracao: dict[str, Any]) -> dict[str, Any]:
    return salvar_configuracao(configuracao)


@router.post("/notificacoes/test/toast")
async def testar_toast() -> dict[str, Any]:
    return _testar_canal_notificacao("toast")


@router.post("/notificacoes/test/sound")
async def testar_sound() -> dict[str, Any]:
    return _testar_canal_notificacao("sound")


@router.post("/notificacoes/test/webhook")
async def testar_webhook() -> dict[str, Any]:
    return _testar_canal_notificacao("webhook")


@router.get("/webhooks/info")
async def obter_info_webhook_receiver(request: Request) -> dict[str, Any]:
    historico = carregar_historico()
    porta = request.url.port or 8000
    return {
        "online": True,
        "url": montar_url_recepcao(porta),
        "ultimos": historico[:10],
    }


@router.post("/webhooks/incoming")
async def receber_webhook(payload: Any = Body(...)) -> dict[str, Any]:
    evento = payload_para_evento(payload)
    historico = registrar_webhook_recebido(payload, evento)
    resultado = registrarEvento(evento)

    return {
        "recebido": True,
        "evento": _model_dump(evento),
        "dispatcher": resultado,
        "total_historico": len(historico),
    }


@router.get("/profiles", response_model=list[ProfileMetadata])
async def list_profiles(request: Request) -> list[dict[str, Any]]:
    try:
        return _manager(request).list_profiles()
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.post("/profiles", response_model=ProfileOperationResponse)
async def create_profile(payload: ProfileCreateRequest, request: Request) -> dict[str, Any]:
    try:
        return {"status": "success", **_manager(request).create_profile(payload.name)}
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.post("/profiles/open", response_model=ProfileOperationResponse)
async def open_profile(payload: ProfileOpenRequest, request: Request) -> dict[str, Any]:
    try:
        return await _manager(request).open_profile(payload.name)
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.put("/profiles/{profile_name}", response_model=ProfileOperationResponse)
async def rename_profile(profile_name: str, payload: ProfileRenameRequest, request: Request) -> dict[str, Any]:
    try:
        return {"status": "success", **await _manager(request).rename_profile(profile_name, payload.new_name)}
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.delete("/profiles/{profile_name}", response_model=ProfileOperationResponse)
async def delete_profile(profile_name: str, request: Request) -> dict[str, Any]:
    try:
        return {"status": "success", **await _manager(request).delete_profile(profile_name)}
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.post("/profiles/default", response_model=ProfileOperationResponse)
async def set_default_profile(payload: ProfileDefaultRequest, request: Request) -> dict[str, Any]:
    try:
        return {"status": "success", **_manager(request).set_default_profile(payload.name)}
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.get("/profiles/export/{profile_name}")
async def export_profile(profile_name: str, request: Request) -> FileResponse:
    try:
        zip_path, zip_name, logs = await _manager(request).export_profile(profile_name)
    except Exception as exc:
        raise _profile_error(exc) from exc

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=zip_name,
        headers={"X-Navyauto-Log": logs[0]["mensagem"] if logs else "Perfil exportado"},
        background=BackgroundTask(lambda: zip_path.exists() and zip_path.unlink()),
    )


@router.post("/profiles/import")
async def import_profile(request: Request, arquivo: UploadFile = File(...)):
    if not arquivo.filename or not arquivo.filename.lower().endswith(".zip"):
        raise HTTPException(400, "Envie um arquivo .zip.")
    content = await arquivo.read()
    if not content:
        raise HTTPException(400, "Arquivo ZIP vazio.")
    try:
        result = await _manager(request).import_profile_zip(content, arquivo.filename)  # passa o nome
        return {"status": "success", **result}
    except Exception as exc:
        raise _profile_error(exc) from exc


@router.get("/flows", response_model=list[str])
async def list_flows(request: Request) -> list[str]:
    flows_dir = _base_dir(request) / "flows"
    flows_dir.mkdir(parents=True, exist_ok=True)
    return sorted(path.name for path in flows_dir.iterdir() if path.is_file() and path.suffix.lower() == ".json")


@router.get("/flows/{flow_name}")
async def load_flow(flow_name: str, request: Request) -> Any:
    flows_dir = _base_dir(request) / "flows"
    flows_dir.mkdir(parents=True, exist_ok=True)
    manager = _manager(request)
    try:
        filename = manager.safe_flow_filename(flow_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    flow_path = flows_dir / filename
    if not flow_path.exists() or not flow_path.is_file():
        raise HTTPException(status_code=404, detail=f"Fluxo nao encontrado: {filename}")

    try:
        return json.loads(flow_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"JSON invalido em {filename}: {exc}") from exc


@router.post("/flows", response_model=FlowSavedResponse)
async def save_flow(payload: FlowSaveRequest, request: Request) -> FlowSavedResponse:
    manager = _manager(request)
    flows_dir = _base_dir(request) / "flows"
    flows_dir.mkdir(parents=True, exist_ok=True)

    data = _model_dump(payload)
    try:
        filename = manager.safe_flow_filename(payload.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    flow_path = flows_dir / filename
    flow_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return FlowSavedResponse(status="success", flow=filename, path=f"flows/{filename}")


@router.post("/run", response_model=RunFlowResponse)
async def run_flow(payload: RunFlowRequest, request: Request) -> dict[str, Any]:
    try:
        flow = payload.flow
        if not flow.endswith(".json"):
            flow += ".json"
        return await _manager(request).run_flow(payload.profile, payload.flow)
    except FileNotFoundError as exc:
        print(exc)
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ValueError, BrowserRunError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha ao executar fluxo: {exc}") from exc


@router.get("/runtime")
async def runtime_status(request: Request) -> dict[str, Any]:
    return await _manager(request).status()


legacy_router = APIRouter()


@legacy_router.get("/status")
async def status(request: Request) -> dict[str, Any]:
    return await _manager(request).status()


@legacy_router.post("/acao/navegar")
async def navegar(payload: ActionNavigate, request: Request) -> dict[str, Any]:
    return await _run_legacy_action(request, [{"action": "navigate", "url": payload.url}])


@legacy_router.post("/acao/preencher")
async def preencher(payload: ActionFill, request: Request) -> dict[str, Any]:
    return await _run_legacy_action(
        request,
        [{"action": "fill", "selector": payload.seletor, "value": payload.valor}],
    )


@legacy_router.post("/acao/clicar")
async def clicar(payload: ActionClick, request: Request) -> dict[str, Any]:
    return await _run_legacy_action(request, [{"action": "click", "selector": payload.seletor}])


async def _run_legacy_action(request: Request, steps: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        manager = _manager(request)
        return await manager.run_actions(manager.default_profile(), steps)
    except (ValueError, BrowserRunError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha na acao direta: {exc}") from exc


def _monitor_manager(request: Request) -> MonitorManager:
    return request.app.state.monitor_manager


@router.get("/monitors")
async def list_monitors(request: Request):
    manager = _monitor_manager(request)
    return [m.model_dump() for m in manager.list_monitors()]


@router.get("/monitors/{monitor_id}")
async def get_monitor(monitor_id: str, request: Request):
    manager = _monitor_manager(request)
    monitor = manager.get_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor não encontrado.")
    
    data = monitor.model_dump()
    # Include list of available snapshots for the detail view
    data["snapshots"] = manager.storage.get_snapshots_list(monitor_id)
    return data


@router.get("/monitors/{monitor_id}/history")
async def get_monitor_history(monitor_id: str, request: Request):
    manager = _monitor_manager(request)
    monitor = manager.get_monitor(monitor_id)
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor não encontrado.")
    return manager.storage.get_history(monitor_id)


@router.get("/monitors/{monitor_id}/snapshot/{file}")
async def get_monitor_snapshot(monitor_id: str, file: str, request: Request):
    manager = _monitor_manager(request)
    snapshot_path = manager.storage.get_snapshot_path(monitor_id, file)
    if not snapshot_path or not snapshot_path.exists():
        raise HTTPException(status_code=404, detail="Snapshot não encontrado.")
    return FileResponse(snapshot_path, media_type="image/png")


@router.post("/monitors/{monitor_id}/start")
async def start_monitor(monitor_id: str, request: Request):
    manager = _monitor_manager(request)
    try:
        await manager.start_monitor(monitor_id)
        return {"status": "success", "message": "Monitor iniciado com sucesso."}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/monitors/{monitor_id}/pause")
async def pause_monitor(monitor_id: str, request: Request):
    manager = _monitor_manager(request)
    try:
        await manager.pause_monitor(monitor_id)
        return {"status": "success", "message": "Monitor pausado com sucesso."}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/monitors/{monitor_id}")
async def delete_monitor(monitor_id: str, request: Request):
    manager = _monitor_manager(request)
    try:
        await manager.remove_monitor(monitor_id)
        return {"status": "success", "message": "Monitor removido com sucesso."}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
