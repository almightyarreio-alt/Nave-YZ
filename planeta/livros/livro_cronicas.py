from datetime import datetime
from pathlib import Path
import json


class LivroCronicas:

    def __init__(self, caminho="planeta/cronicas/universal.jsonl"):

        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)


    def registrar(self, cronica):

        cronica["data"] = datetime.now().isoformat()

        with self.caminho.open("a", encoding="utf-8") as arquivo:

            arquivo.write(
                json.dumps(cronica,ensure_ascii=False)+ "\n"
            )