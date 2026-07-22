"""
👤 Cronista

Primeiro Habitante do Planeta.

Responsabilidade:
Registrar acontecimentos relevantes no Livro de Crônicas.

Não deve:

- alterar estados do planeta;
- executar automações;
- tomar decisões;
- criar acontecimentos.

Sua única missão é preservar a história do Planeta.
"""

from habitantes.habitante import Habitante


class Cronista(Habitante):

    """
    Historiador oficial do Planeta.

    Responsável por registrar
    acontecimentos relevantes.
    """

    def __init__(self, planeta, livro):

        super().__init__(planeta=planeta, nome="Cronista", missao="Preservar a história do planeta.")

        self.livro = livro
        self.capacidades.extend([
            "registrar",
            "consultar",
            "buscar",
            "estatisticas",
            "exportar",
        ])

    def registrar(self, origem, evento, descricao, dados=None):

        """
        Registra acontecimentos relevantes no Livro de Crônicas.
        """
        cronica = {
            "origem": origem,
            "evento": evento,
            "descricao": descricao,
            "dados": dados or {}
            }

        self.livro.registrar(cronica)