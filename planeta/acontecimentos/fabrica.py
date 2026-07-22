"""
🏭 Fábrica de Acontecimentos

Responsável pela criação oficial de acontecimentos do Planeta.

Toda ocorrência deve nascer através desta fábrica.

A fábrica garante que somente acontecimentos reconhecidos pelo
Catálogo Oficial sejam criados.
"""

from __future__ import annotations

from typing import Any

from .acontecimento import Acontecimento
from .catalogo import DefinicaoAcontecimento


class FabricaAcontecimentos:
    """
    Criador oficial de acontecimentos.
    """

    def criar(
        self,
        definicao: DefinicaoAcontecimento,
        origem: dict[str, Any],
        dados: dict[str, Any] | None = None,
        contexto: dict[str, Any] | None = None,
        descricao: str | None = None,
    ) -> Acontecimento:
        """
        Cria um novo acontecimento válido.
        """

        self._validar_origem(origem)

        return Acontecimento(

            definicao=definicao,

            origem=origem,

            dados=dados or {},

            contexto=contexto or {},

            descricao=descricao,
        )


    def _validar_origem(
        self,
        origem: dict[str, Any]
    ) -> None:
        """
        Garante que todo acontecimento possui uma origem.
        """

        if not origem:

            raise ValueError(
                "Todo acontecimento deve possuir uma origem."
            )


fabrica = FabricaAcontecimentos()