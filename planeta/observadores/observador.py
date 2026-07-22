"""
👁 Entidade base dos Observadores

Todo observador do planeta deve possuir:
- identidade
- domínio
- missão
- estado
"""


from datetime import datetime


class Observador:

    def __init__(
        self,
        nome: str,
        dominio: str,
        missao: str
    ):

        self.nome = nome
        self.dominio = dominio
        self.missao = missao

        self.estado = "inativo"

        self.nascimento = datetime.now()


    def ativar(self):

        self.estado = "ativo"


    def desativar(self):

        self.estado = "inativo"


    def observar(self, sinal):

        """
        Método obrigatório.

        Cada observador deve definir
        como interpreta um sinal.
        """

        raise NotImplementedError(
            "Todo observador precisa implementar observar()."
        )


    def identidade(self):

        return {

            "nome": self.nome,

            "dominio": self.dominio,

            "missao": self.missao,

            "estado": self.estado

        }