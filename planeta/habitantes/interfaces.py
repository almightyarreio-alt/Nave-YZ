from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Protocol
from pathlib import Path

class LeisProtocol(Protocol):
    """Contrato para o sistema de Leis."""
    def permite(self, acao: str, contexto: Dict[str, Any]) -> bool: ...
    def obter_regra(self, acao: str) -> Dict[str, Any]: ...

class MemoriaProtocol(Protocol):
    """Contrato para o sistema de Memória."""
    def recuperar(self, chave: str) -> Optional[Any]: ...
    def armazenar(self, chave: str, valor: Any) -> None: ...
    def remover(self, chave: str) -> None: ...
    def listar(self, prefixo: str) -> list: ...

class CronicaProtocol(Protocol):
    """Contrato para o sistema de Crônicas."""
    def registrar(self, origem: Dict, evento: str, descricao: str, dados: Dict) -> None: ...

class Habitante:

    def __init__(
        self,
        leis,
        memoria,
        cronista
    ):
        self.leis = leis
        self.memoria = memoria
        self.cronista = cronista

# class HabitantePerfil(Habitante):

#     def criar(...):

#     def remover(...):

#     def localizar(...):

# class HabitanteNavegador(Habitante):

#     def iniciar()

#     def navegar()

#     def clicar()

#     def fechar()