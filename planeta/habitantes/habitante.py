"""
👤 Habitante

Classe base de todos os habitantes do ArreioWork.

Todo habitante possui identidade,
estado, missão e pertence a um planeta.
"""

from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from planeta.planeta import Planeta


class Habitante(ABC):

    ESTADOS = (
        "criado",
        "adormecido",
        "ativo",
        "ocupado",
        "suspenso",
        "encerrado",
    )

    def __init__(
        self,
        planeta: Planeta,
        nome: str,
        missao: str,
    ):

        self.planeta = planeta

        self.nome = nome

        self.tipo = self.__class__.__name__

        self.missao = missao

        self.estado = "criado"

        self.nascimento = datetime.now()

        self.capacidades: list[str] = []

    # ------------------------------------
    # Consciência
    # ------------------------------------

    def quem_sou(self):

        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "missao": self.missao,
        }

    def diagnostico(self):

        return {
            "estado": self.estado,
            "capacidades": self.capacidades,
        }

    # ------------------------------------
    # Ciclo de Vida
    # ------------------------------------

    def despertar(self):

        self.estado = "ativo"

    def suspender(self):

        self.estado = "suspenso"

    def encerrar(self):

        self.estado = "encerrado"

    # ------------------------------------
    # Crônicas
    # ------------------------------------

    def registrar_cronica(
        self,
        evento: str,
        descricao: str,
        dados: dict | None = None,
    ):

        if self.planeta.cronista is None:
            return

        self.planeta.cronista.registrar(
            origem={
                "tipo": self.tipo,
                "nome": self.nome,
            },
            evento=evento,
            descricao=descricao,
            dados=dados,
        )