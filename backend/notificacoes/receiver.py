import json
import socket
from datetime import datetime
from pathlib import Path
from typing import Any

from .evento import EventoNotificacao


CAMINHO_HISTORICO = Path(__file__).with_name("webhooks_recebidos.json")
LIMITE_HISTORICO = 50


def detectar_ip_local() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as conexao:
            conexao.connect(("8.8.8.8", 80))
            return conexao.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())


def montar_url_recepcao(porta: int = 8000) -> str:
    return f"http://{detectar_ip_local()}:{porta}/api/webhooks/incoming"


def carregar_historico() -> list[dict[str, Any]]:
    if not CAMINHO_HISTORICO.exists():
        return []

    try:
        with CAMINHO_HISTORICO.open("r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)
            return historico if isinstance(historico, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def registrar_webhook_recebido(payload: Any, evento: EventoNotificacao) -> list[dict[str, Any]]:
    historico = carregar_historico()
    historico.insert(
        0,
        {
            "recebido_em": datetime.now().isoformat(timespec="seconds"),
            "payload": payload,
            "evento": _evento_para_dict(evento),
        },
    )
    historico = historico[:LIMITE_HISTORICO]

    with CAMINHO_HISTORICO.open("w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")

    return historico


def payload_para_evento(payload: Any) -> EventoNotificacao:
    if not isinstance(payload, dict):
        payload = {"payload": payload}

    titulo = payload.get("titulo") or payload.get("title") or payload.get("evento") or "Webhook Recebido"
    mensagem = payload.get("mensagem") or payload.get("message") or payload.get("descricao")

    if not mensagem:
        mensagem = json.dumps(payload, ensure_ascii=False)[:240]

    return EventoNotificacao(
        tipo=str(payload.get("tipo") or payload.get("type") or "info"),
        titulo=str(titulo),
        mensagem=str(mensagem),
    )


def _evento_para_dict(evento: EventoNotificacao) -> dict[str, Any]:
    if hasattr(evento, "model_dump"):
        return evento.model_dump()
    return evento.dict()
