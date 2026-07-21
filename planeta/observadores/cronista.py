import json
import uuid

from pathlib import Path
from datetime import datetime, timezone


class CronistaUniversal:

    def __init__(self):

        self.arquivo_cronicas = (
            Path(__file__)
            .parent.parent
            / "cronicas"
            / "universal.jsonl"
        )

        self.arquivo_cronicas.parent.mkdir(
            parents=True,
            exist_ok=True
        )


    def registrar(
        self,
        origem: dict,
        evento: str,
        descricao: str,
        dados: dict | None = None,
        nivel: str = "INFO"
    ):

        registro = {

            "id": f"evt_{uuid.uuid4().hex[:12]}",

            "momento": datetime.now(
                timezone.utc
            ).isoformat(),

            "origem": origem,

            "evento": evento,

            "nivel": nivel,

            "descricao": descricao,

            "dados": dados or {}
        }


        with open(
            self.arquivo_cronicas,
            "a",
            encoding="utf-8"
        ) as arquivo:

            arquivo.write(
                json.dumps(
                    registro,
                    ensure_ascii=False
                )
                + "\n"
            )


        return registro



cronista = CronistaUniversal()