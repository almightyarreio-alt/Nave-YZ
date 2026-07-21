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

class HabitanteInterface(ABC):
    """Interface base para todos os Habitantes."""
    
    @abstractmethod
    def profissao(self) -> str:
        """Retorna a profissão do Habitante."""
        pass
    
    @abstractmethod
    def despertar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Desperta o Habitante para o trabalho."""
        pass
    
    @abstractmethod
    def executar(self, acao: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma ação específica."""
        pass
    
    @abstractmethod
    def recolher(self) -> Dict[str, Any]:
        """Recolhe o Habitante ao descanso."""
        pass
    
    @abstractmethod
    def esta_desperto(self) -> bool:
        """Verifica se o Habitante está desperto."""
        pass