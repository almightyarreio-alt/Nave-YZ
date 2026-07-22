"""
📚 Catálogo de Acontecimentos

Contém as definições oficiais dos acontecimentos reconhecidos pelo
Planeta.

Todo acontecimento registrado deve estar previamente definido neste
catálogo.

O Catálogo representa o vocabulário oficial do Planeta.
"""

from __future__ import annotations

from dataclasses import dataclass

from .categorias import Categoria
from .severidades import Severidade


@dataclass(frozen=True, slots=True)
class DefinicaoAcontecimento:
    """
    Define um acontecimento reconhecido oficialmente pelo Planeta.
    """

    codigo: str
    categoria: Categoria
    severidade: Severidade
    descricao: str


class Catalogo:
    """
    Catálogo Oficial de Acontecimentos.
    """

    # ==========================================================
    # VIDA DO PLANETA
    # ==========================================================

    PLANETA_CRIADO = DefinicaoAcontecimento(
        codigo="planeta_criado",
        categoria=Categoria.VIDA,
        severidade=Severidade.INFO,
        descricao="O planeta foi criado."
    )

    PLANETA_DESPERTOU = DefinicaoAcontecimento(
        codigo="planeta_despertou",
        categoria=Categoria.VIDA,
        severidade=Severidade.INFO,
        descricao="O planeta iniciou seu funcionamento."
    )

    PLANETA_SUSPENSO = DefinicaoAcontecimento(
        codigo="planeta_suspenso",
        categoria=Categoria.VIDA,
        severidade=Severidade.AVISO,
        descricao="O planeta entrou em estado suspenso."
    )

    PLANETA_ENCERRADO = DefinicaoAcontecimento(
        codigo="planeta_encerrado",
        categoria=Categoria.VIDA,
        severidade=Severidade.INFO,
        descricao="O planeta encerrou suas atividades."
    )

    # ==========================================================
    # HABITANTES
    # ==========================================================

    HABITANTE_CRIADO = DefinicaoAcontecimento(
        codigo="habitante_criado",
        categoria=Categoria.HABITANTE,
        severidade=Severidade.INFO,
        descricao="Um novo habitante passou a existir."
    )

    HABITANTE_DESPERTOU = DefinicaoAcontecimento(
        codigo="habitante_despertou",
        categoria=Categoria.HABITANTE,
        severidade=Severidade.INFO,
        descricao="Um habitante iniciou suas atividades."
    )

    HABITANTE_SUSPENSO = DefinicaoAcontecimento(
        codigo="habitante_suspenso",
        categoria=Categoria.HABITANTE,
        severidade=Severidade.AVISO,
        descricao="Um habitante entrou em estado suspenso."
    )

    HABITANTE_ENCERRADO = DefinicaoAcontecimento(
        codigo="habitante_encerrado",
        categoria=Categoria.HABITANTE,
        severidade=Severidade.INFO,
        descricao="Um habitante encerrou suas atividades."
    )

    # ==========================================================
    # PORTAIS
    # ==========================================================

    PORTAL_ABERTO = DefinicaoAcontecimento(
        codigo="portal_aberto",
        categoria=Categoria.PORTAL,
        severidade=Severidade.INFO,
        descricao="Um portal foi disponibilizado."
    )

    PORTAL_FECHADO = DefinicaoAcontecimento(
        codigo="portal_fechado",
        categoria=Categoria.PORTAL,
        severidade=Severidade.INFO,
        descricao="Um portal foi encerrado."
    )

    # ==========================================================
    # EXECUÇÕES
    # ==========================================================

    EXECUCAO_INICIADA = DefinicaoAcontecimento(
        codigo="execucao_iniciada",
        categoria=Categoria.EXECUCAO,
        severidade=Severidade.INFO,
        descricao="Uma execução foi iniciada."
    )

    EXECUCAO_CONCLUIDA = DefinicaoAcontecimento(
        codigo="execucao_concluida",
        categoria=Categoria.EXECUCAO,
        severidade=Severidade.INFO,
        descricao="Uma execução foi concluída."
    )

    EXECUCAO_INTERROMPIDA = DefinicaoAcontecimento(
        codigo="execucao_interrompida",
        categoria=Categoria.EXECUCAO,
        severidade=Severidade.AVISO,
        descricao="Uma execução foi interrompida."
    )

    # ==========================================================
    # SISTEMA
    # ==========================================================

    ERRO = DefinicaoAcontecimento(
        codigo="erro",
        categoria=Categoria.SISTEMA,
        severidade=Severidade.ERRO,
        descricao="Ocorreu um erro durante a operação."
    )

    FALHA_CRITICA = DefinicaoAcontecimento(
        codigo="falha_critica",
        categoria=Categoria.SISTEMA,
        severidade=Severidade.CRITICO,
        descricao="Ocorreu uma falha crítica."
    )

    @classmethod
    def todos(cls) -> list[DefinicaoAcontecimento]:
        """
        Retorna todas as definições oficiais do catálogo.
        """

        return [
            valor
            for valor in vars(cls).values()
            if isinstance(valor, DefinicaoAcontecimento)
        ]

    @classmethod
    def buscar(cls, codigo: str) -> DefinicaoAcontecimento | None:
        """
        Busca uma definição pelo código oficial.
        """

        for definicao in cls.todos():
            if definicao.codigo == codigo:
                return definicao

        return None

    @classmethod
    def existe(cls, codigo: str) -> bool:
        """
        Verifica se um código existe no catálogo.
        """

        return cls.buscar(codigo) is not None