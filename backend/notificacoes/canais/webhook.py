import json
from urllib import request


CANAL = "webhook"


class Webhook:
    def __init__(self, config):
        self.config = config

    def enviar(self, evento):
        url = self.config.get("url", "").strip()
        if not url:
            return {"mensagem": "Webhook sem URL configurada"}

        payload = evento.model_dump() if hasattr(evento, "model_dump") else evento.dict()
        dados = json.dumps(payload).encode("utf-8")
        requisicao = request.Request(
            url,
            data=dados,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(requisicao, timeout=10) as resposta:
            return {"status": resposta.status}


def criar_canal(config):
    return Webhook(config)
