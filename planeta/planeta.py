"""
🪐 Planeta Nave YZ

Entidade raiz do ArreioWork.

Responsável por:
- existir;
- conhecer sua identidade;
- controlar seu ciclo de vida;
- registrar sua própria história;
- avaliar seu estado.

Não conhece:
- APIs;
- FastAPI;
- usuários;
- tecnologias externas.
"""

from datetime import datetime
from typing import Optional


class Planeta:
    """
    Representa um planeta dentro do Universo ArreioWork.
    Um planeta é uma entidade independente capaz de:
    - nascer;
    - despertar;
    - manter consciência básica;
    - registrar sua evolução.
    """

    ESTADOS_VALIDOS = [
        "criado",
        "adormecido",
        "despertando",
        "ativo",
        "suspenso",
        "encerrado",
    ]

    def __init__(self, nome: str, tipo: str, proposito: str, universo: str = "ArreioWork", constelacao: Optional[str] = None,):

        # ==========================
        # Identidade
        # ==========================

        self.nome = nome
        self.tipo = tipo
        self.proposito = proposito

        # ==========================
        # Ambiente
        # ==========================

        self.universo = universo
        self.constelacao = constelacao

        # ==========================
        # Estado
        # ==========================

        self.estado = "criado"
        self.nascimento = None
        self.ultimo_evento = None

        # ==========================
        # Consciência
        # ==========================

        self.memoria = []
        self.saude = "desconhecida"


    # ==================================================
    # Ciclo de vida
    # ==================================================

    def despertar(self):

        """
        Inicia a existência operacional do planeta.
        """

        if self.estado == "ativo":
            return

        self._mudar_estado(novo_estado="despertando")        
        self.nascimento = datetime.now()


        self.registrar_cronica(evento="nascimento", 
                               descricao=(f"O planeta {self.nome} iniciou sua existência."))

        self._mudar_estado(novo_estado="ativo")

        self.saude = "saudavel"

    def suspender(self):
        """
        Coloca o planeta em estado suspenso.
        """
        self._mudar_estado("suspenso")
        self.registrar_cronica(evento="suspensao", descricao="O planeta entrou em modo suspenso.")


    def encerrar(self):
        """
        Finaliza o ciclo de vida do planeta.
        """
        self._mudar_estado("encerrado")
        self.registrar_cronica(evento="encerramento", descricao="O planeta encerrou suas atividades.")


    # ==================================================
    # Consciência
    # ==================================================

    def quem_sou(self):
        """
        Retorna a identidade do planeta.
        """
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "proposito": self.proposito,
        }


    def onde_existo(self):
        """
        Retorna o ambiente de existência.
        """

        return {
            "universo": self.universo,
            "constelacao": self.constelacao,
        }


    def diagnostico(self):
        """
        Avalia a condição atual do planeta.
        """
        return {
            "nome": self.nome,
            "estado": self.estado,
            "saude": self.saude,
            "ultimo_evento": self.ultimo_evento,
            "cronicas": len(self.memoria),
        }


    # ==================================================
    # Crônicas
    # ==================================================

    def registrar_cronica(self, evento: str, descricao: str,):
        """
        Registra acontecimentos importantes.
        """

        cronica = {
            "origem": {
                "tipo": "planeta",
                "nome": self.nome,
            },
            "evento": evento,
            "descricao": descricao,
            "estado": self.estado,
            "data": datetime.now().isoformat(),
        }


        self.memoria.append(
            cronica
        )


        self.ultimo_evento = evento


    # ==================================================
    # Estado interno
    # ==================================================

    def _mudar_estado(self, novo_estado: str):
        """
        Controla transições de estado.
        """

        if novo_estado not in self.ESTADOS_VALIDOS:

            raise ValueError(f"Estado inválido: {novo_estado}")

        self.estado = novo_estado


    def esta_ativo(self):

        return self.estado == "ativo"