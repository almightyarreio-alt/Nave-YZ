"""
📣 Acontecimento

Representa um fato ocorrido no Planeta.

Um Acontecimento é uma ocorrência concreta baseada em uma definição
oficial presente no Catálogo de Acontecimentos.

Ele ainda não faz parte da história oficial.

Somente após ser registrado pelo Cronista torna-se uma Crônica.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from .catalogo import DefinicaoAcontecimento


@dataclass(frozen=True, slots=True)
class Acontecimento:
    """
    Representa um acontecimento ocorrido.
    """

    definicao: DefinicaoAcontecimento

    origem: dict[str, Any]

    dados: dict[str, Any] = field(default_factory=dict)

    contexto: dict[str, Any] = field(default_factory=dict)

    descricao: str | None = None

    id: str = field(default_factory=lambda: str(uuid4()))

    momento: datetime = field(default_factory=datetime.now)

    @property
    def codigo(self) -> str:
        return self.definicao.codigo

    @property
    def categoria(self):
        return self.definicao.categoria

    @property
    def severidade(self):
        return self.definicao.severidade

    @property
    def descricao_final(self) -> str:
        """
        Retorna a descrição personalizada, caso exista,
        ou a descrição oficial do Catálogo.
        """
        return self.descricao or self.definicao.descricao

    def to_dict(self) -> dict[str, Any]:
        """
        Serializa o acontecimento.
        """

        return {

            "id": self.id,

            "momento": self.momento.isoformat(),

            "codigo": self.codigo,

            "categoria": self.categoria.value,

            "severidade": self.severidade.value,

            "origem": self.origem,

            "descricao": self.descricao_final,

            "dados": self.dados,

            "contexto": self.contexto,
        }