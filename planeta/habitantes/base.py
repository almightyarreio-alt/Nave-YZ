from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

from .interfaces import LeisProtocol, MemoriaProtocol, CronicaProtocol
from .excecoes import HabitanteAdormecido, ViolacaoLeis

class HabitanteBase(ABC):
    """Classe base para todos os Habitantes do planeta."""
    
    def __init__(
        self,
        leis: LeisProtocol,
        memoria: MemoriaProtocol,
        cronica: CronicaProtocol
    ):
        self._leis = leis
        self._memoria = memoria
        self._cronica = cronica
        self._nome: Optional[str] = None
        self._identidade: Optional[str] = None
        self._esta_desperto = False
        self._correlation_id: Optional[str] = None
        self._timestamp_inicio: Optional[datetime] = None
    
    @property
    def nome(self) -> str:
        """Retorna o nome do Habitante."""
        if not self._nome:
            raise HabitanteAdormecido("Habitante sem nome")
        return self._nome
    
    @property
    def identidade(self) -> str:
        """Retorna a identidade do Habitante."""
        if not self._identidade:
            raise HabitanteAdormecido("Habitante sem identidade")
        return self._identidade
    
    @abstractmethod
    def profissao(self) -> str:
        """Retorna a profissão do Habitante."""
        pass
    
    def esta_desperto(self) -> bool:
        """Verifica se o Habitante está desperto."""
        return self._esta_desperto
    
    def _validar_acao(self, acao: str, contexto: Dict[str, Any]) -> None:
        """Valida se a ação é permitida pelas Leis."""
        if not self._leis.permite(acao, contexto):
            raise ViolacaoLeis(acao, "Ação não permitida pelas Leis")
    
    def _gerar_correlation_id(self) -> str:
        """Gera um ID de correlação para rastreamento."""
        return str(uuid.uuid4())
    
    def _registrar_evento(
        self,
        evento: str,
        descricao: str,
        dados: Optional[Dict] = None,
        origem: Optional[Dict] = None
    ) -> None:
        """Registra um evento no sistema de Crônicas."""
        self._cronica.registrar(
            origem=origem or {
                "tipo": "Habitante",
                "nome": self._nome or "Desconhecido",
                "profissao": self.profissao()
            },
            evento=evento,
            descricao=descricao,
            dados={
                **(dados or {}),
                "correlation_id": self._correlation_id,
                "habitante": self._nome,
                "profissao": self.profissao()
            }
        )
    
    def _recuperar_estado(self, chave: str) -> Optional[Any]:
        """Recupera estado da Memória compartilhada."""
        return self._memoria.recuperar(f"{self.profissao()}_{chave}")
    
    def _armazenar_estado(self, chave: str, valor: Any) -> None:
        """Armazena estado na Memória compartilhada."""
        self._memoria.armazenar(
            f"{self.profissao()}_{chave}",
            valor
        )
    
    def despertar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Desperta o Habitante para o trabalho."""
        if self._esta_desperto:
            return {
                "sucesso": True,
                "mensagem": f"Habitante '{self._nome}' já está desperto",
                "habitante": self._nome,
                "profissao": self.profissao()
            }
        
        # Validar ação
        self._validar_acao("despertar", contexto)
        
        # Configurar identidade
        self._nome = contexto.get("nome", "Desconhecido")
        self._identidade = contexto.get("identidade")
        self._correlation_id = self._gerar_correlation_id()
        self._timestamp_inicio = datetime.now()
        
        # Registrar evento
        self._registrar_evento(
            evento="despertar",
            descricao=f"O Habitante {self.profissao()} '{self._nome}' despertou",
            dados={
                "identidade": self._identidade,
                "contexto": contexto
            }
        )
        
        self._esta_desperto = True
        
        return {
            "sucesso": True,
            "mensagem": f"Habitante '{self._nome}' despertou com sucesso",
            "habitante": self._nome,
            "profissao": self.profissao(),
            "identidade": self._identidade,
            "correlation_id": self._correlation_id
        }
    
    def recolher(self) -> Dict[str, Any]:
        """Recolhe o Habitante ao descanso."""
        if not self._esta_desperto:
            return {
                "sucesso": True,
                "mensagem": "Habitante já está recolhido"
            }
        
        # Registrar evento
        self._registrar_evento(
            evento="recolher",
            descricao=f"O Habitante {self.profissao()} '{self._nome}' foi recolhido",
            dados={
                "tempo_ativo": str(datetime.now() - self._timestamp_inicio)
            }
        )
        
        # Limpar estado
        self._esta_desperto = False
        self._nome = None
        self._identidade = None
        self._correlation_id = None
        self._timestamp_inicio = None
        
        return {
            "sucesso": True,
            "mensagem": "Habitante recolhido com sucesso",
            "profissao": self.profissao()
        }
    
    @abstractmethod
    def executar(self, acao: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma ação específica do Habitante."""
        pass