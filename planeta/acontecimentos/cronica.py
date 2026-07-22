"""
📜 Crônica

Representa o registro oficial de um acontecimento.

Uma Crônica é criada exclusivamente pelo Cronista e passa a compor
a história permanente do Planeta.

Uma vez criada, jamais deve ser alterada.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from .acontecimento import Acontecimento


@dataclass(frozen=True, slots=True)
class Cronica:
    """
    Documento histórico oficial do Planeta.
    """

    acontecimento: Acontecimento

    registrado_por: str = "Cronista"

    registrada_em: datetime = field(default_factory=datetime.now)

    id: str = field(default_factory=lambda: str(uuid4()))

    versao: int = 1

    @property
    def codigo(self) -> str:
        return self.acontecimento.codigo

    @property
    def categoria(self):
        return self.acontecimento.categoria

    @property
    def severidade(self):
        return self.acontecimento.severidade

    def to_dict(self) -> dict[str, Any]:
        """
        Serializa a Crônica.
        """

        return {

            "id": self.id,

            "versao": self.versao,

            "registrado_por": self.registrado_por,

            "registrada_em": self.registrada_em.isoformat(),

            "acontecimento": self.acontecimento.to_dict()
        }