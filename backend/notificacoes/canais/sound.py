import sys
from pathlib import Path


CANAL = "sound"


PASTA_SONS = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "sons"
)


class Sound:

    def __init__(self, config):
        self.config = config


    def enviar(self, evento):

        arquivo = self.config.get(
            "file",
            "alert.wav"
        )


        caminho = (
            PASTA_SONS /
            arquivo
        )


        if sys.platform == "win32":

            import winsound


            if caminho.exists():

                winsound.PlaySound(
                    str(caminho),
                    winsound.SND_FILENAME |
                    winsound.SND_ASYNC
                )

                return {
                    "mensagem": "Som executado",
                    "arquivo": arquivo
                }


            winsound.MessageBeep()

            return {
                "mensagem": "Arquivo não encontrado",
                "arquivo": arquivo
            }


        return {
            "mensagem":
            "Som indisponível"
        }



def criar_canal(config):

    return Sound(config)