import importlib
import pkgutil

from .config import carregar_configuracao
from .evento import EventoNotificacao
from . import canais


def _normalizar_evento(evento):
    if isinstance(evento, EventoNotificacao):
        return evento
    return EventoNotificacao(**evento)


def _carregar_canais(configuracao):
    for modulo_info in pkgutil.iter_modules(canais.__path__):
        if modulo_info.name.startswith("_"):
            continue

        modulo = importlib.import_module(f"{canais.__name__}.{modulo_info.name}")
        nome_canal = getattr(modulo, "CANAL", modulo_info.name)
        config_canal = configuracao.get(nome_canal, {})

        if not config_canal.get("enabled", False):
            continue

        criar_canal = getattr(modulo, "criar_canal", None)
        if criar_canal:
            yield nome_canal, criar_canal(config_canal)


def registrarEvento(evento):
    evento_notificacao = _normalizar_evento(evento)
    configuracao = carregar_configuracao()

    if not configuracao.get("notifications", {}).get("enabled", False):
        return {"enviado": False, "canais": []}

    resultados = []
    for nome_canal, canal in _carregar_canais(configuracao):
        try:
            resultado = canal.enviar(evento_notificacao)
            resultados.append({"canal": nome_canal, "sucesso": True, "resultado": resultado})
        except Exception as erro:
            resultados.append({"canal": nome_canal, "sucesso": False, "erro": str(erro)})

    return {"enviado": True, "canais": resultados}
