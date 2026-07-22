"""
🏷 Categorias de Acontecimentos

Classificam a natureza dos acontecimentos reconhecidos pelo Planeta.

As categorias permitem organizar Crônicas, métricas, auditorias,
estatísticas e observabilidade.
"""

from enum import Enum


class Categoria(str, Enum):
    """
    Categorias oficiais do ArreioWork.
    """

    VIDA = "vida"

    SOCIEDADE = "sociedade"

    COMUNICACAO = "comunicacao"

    MEMORIA = "memoria"

    CONHECIMENTO = "conhecimento"

    EXECUCAO = "execucao"

    OBSERVACAO = "observacao"

    IDENTIDADE = "identidade"

    LEIS = "leis"

    SEGURANCA = "seguranca"

    CIVILIZACAO = "civilizacao"

    HABITANTE = "habitante"

    PORTAL = "portal"

    SISTEMA = "sistema"
