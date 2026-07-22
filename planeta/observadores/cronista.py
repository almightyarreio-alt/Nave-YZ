"""
📜 Cronista

Primeiro Observador da Nave YZ.

Responsável por registrar
aquilo que o planeta percebe.
"""


from .observador import Observador


class Cronista(Observador):


    def __init__(self):

        super().__init__(

            nome="Cronista",

            dominio="SISTEMA",

            missao="Registrar acontecimentos do planeta"

        )

        self.registros = []



    def observar(self, sinal):

        registro = {

            "observador": self.nome,

            "sinal": sinal.to_dict()

        }


        self.registros.append(
            registro
        )


        return registro



    def historico(self):

        return self.registros