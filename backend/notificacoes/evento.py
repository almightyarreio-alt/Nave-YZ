from pydantic import BaseModel


class EventoNotificacao(BaseModel):
    tipo: str = "info"
    titulo: str
    mensagem: str
