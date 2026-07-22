"""
📡 Sinais

Representam percepções brutas
dos observadores.
"""


from datetime import datetime
import uuid


class Sinal:


    def __init__(
        self,
        tipo: str,
        origem: str,
        dados: dict | None = None
    ):

        self.id = str(uuid.uuid4())

        self.momento = datetime.now()

        self.tipo = tipo

        self.origem = origem

        self.dados = dados or {}



    def to_dict(self):

        return {

            "id": self.id,

            "momento": self.momento.isoformat(),

            "tipo": self.tipo,

            "origem": self.origem,

            "dados": self.dados

        }