from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime
import json

from playwright.sync_api import (
    sync_playwright,
    BrowserContext,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError
)

from .habitante import HabitanteBase
from .interfaces import LeisProtocol, MemoriaProtocol, CronicaProtocol
from .excecoes import (
    HabitanteAdormecido,
    ViolacaoLeis,
    NavegacaoErro,
    ElementoNaoEncontrado,
    AcaoInvalida
)


class HabitanteNavegador(HabitanteBase):
    """
    Habitante especialista em controlar navegadores web.
    
    Profissão: Navegador
    Responsabilidades:
        - Gerenciar ciclo de vida do navegador
        - Navegar para URLs
        - Interagir com elementos da página
        - Capturar screenshots
        - Extrair informações
    """
    
    # Constantes
    URL_INICIAL = "https://google.com"
    TIMEOUT_PADRAO = 30000  # 30 segundos
    DIRETORIO_IDENTIDADES = "identidades"
    
    # Ações permitidas
    ACOES_PERMITIDAS = {
        "viajar": "Navegar para uma URL",
        "observar": "Obter informações da página atual",
        "esperar_elemento": "Aguardar um elemento aparecer",
        "capturar_tela": "Capturar screenshot",
        "preencher_formulario": "Preencher campos de formulário",
        "clicar": "Clicar em um elemento",
        "extrair_dados": "Extrair dados estruturados",
        "voltar": "Voltar para página anterior",
        "recarregar": "Recarregar página atual"
    }
    
    def __init__(
        self,
        leis: LeisProtocol,
        memoria: MemoriaProtocol,
        cronica: CronicaProtocol
    ):
        super().__init__(leis, memoria, cronica)
        
        # Estado do navegador
        self._playwright: Optional[Playwright] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        
        # Configurações
        self._headless = False
        self._timeout = self.TIMEOUT_PADRAO
        self._historico = []
        self._ultima_acao = None
    
    def profissao(self) -> str:
        return "Navegador"
    
    @property
    def page(self) -> Page:
        """Retorna a página atual, lançando erro se não disponível."""
        if not self._page:
            raise HabitanteAdormecido(self._nome or "Navegador")
        return self._page
    
    @property
    def context(self) -> BrowserContext:
        """Retorna o contexto atual, lançando erro se não disponível."""
        if not self._context:
            raise HabitanteAdormecido(self._nome or "Navegador")
        return self._context
    
    # ==================== MÉTODOS PÚBLICOS ====================
    
    def despertar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Desperta o Habitante e inicializa o navegador."""
        # Chama o despertar base
        resultado_base = super().despertar(contexto)
        
        if resultado_base.get("sucesso") and not self._playwright:
            try:
                self._inicializar_navegador(contexto)
            except Exception as e:
                self._registrar_evento(
                    evento="erro_inicializacao",
                    descricao=f"Falha ao inicializar navegador: {str(e)}",
                    dados={"erro": str(e)}
                )
                raise
        
        return resultado_base
    
    def executar(self, acao: str, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma ação específica do navegador.
        
        Ações disponíveis:
            - viajar: Navegar para URL
            - observar: Obter informações da página
            - esperar_elemento: Aguardar elemento
            - capturar_tela: Screenshot
            - preencher_formulario: Preencher formulário
            - clicar: Clicar em elemento
            - extrair_dados: Extrair dados
            - voltar: Voltar página
            - recarregar: Recarregar página
        """
        # Validar ação
        if acao not in self.ACOES_PERMITIDAS:
            raise AcaoInvalida(acao, list(self.ACOES_PERMITIDAS.keys()))
        
        # Validar pelas Leis
        self._validar_acao(acao, contexto)
        
        # Validar estado
        if not self._esta_desperto:
            raise HabitanteAdormecido(self._nome or "Navegador")
        
        # Executar ação
        metodo = getattr(self, f"_{acao}", None)
        if not metodo:
            raise NavegacaoErro(acao, "Método não implementado")
        
        try:
            resultado = metodo(contexto)
            self._ultima_acao = acao
            
            # Registrar execução
            self._registrar_evento(
                evento=f"executar_{acao}",
                descricao=f"Executou ação '{acao}'",
                dados=contexto
            )
            
            return {
                "sucesso": True,
                "acao": acao,
                "resultado": resultado,
                "habitante": self._nome,
                "profissao": self.profissao()
            }
            
        except Exception as e:
            # Registrar erro
            self._registrar_evento(
                evento=f"erro_{acao}",
                descricao=f"Erro ao executar '{acao}': {str(e)}",
                dados={"erro": str(e), "contexto": contexto}
            )
            raise
    
    def recolher(self) -> Dict[str, Any]:
        """Recolhe o Habitante e fecha o navegador."""
        try:
            if self._context:
                self._context.close()
            if self._playwright:
                self._playwright.stop()
        except Exception as e:
            self._registrar_evento(
                evento="erro_recolher",
                descricao=f"Erro ao recolher: {str(e)}",
                dados={"erro": str(e)}
            )
        
        self._playwright = None
        self._context = None
        self._page = None
        
        return super().recolher()
    
    # ==================== AÇÕES ESPECÍFICAS ====================
    
    def _viajar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Navega para uma URL."""
        destino = contexto.get("destino")
        if not destino:
            raise NavegacaoErro("destino não informado", "URL não fornecida")
        
        # Garantir protocolo
        if not destino.startswith(("http://", "https://")):
            destino = f"https://{destino}"
        
        timeout = contexto.get("timeout", self._timeout)
        
        try:
            self.page.goto(destino, timeout=timeout)
            
            # Atualizar histórico
            self._historico.append({
                "url": destino,
                "timestamp": datetime.now().isoformat(),
                "titulo": self.page.title()
            })
            
            # Armazenar na Memória
            self._armazenar_estado("ultima_visita", {
                "url": destino,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "url": destino,
                "titulo": self.page.title(),
                "status": "sucesso"
            }
            
        except PlaywrightTimeoutError:
            raise NavegacaoErro(destino, "Timeout ao carregar página")
        except Exception as e:
            raise NavegacaoErro(destino, str(e))
    
    def _observar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém informações da página atual."""
        return {
            "url": self.page.url,
            "titulo": self.page.title(),
            "conteudo": self.page.content() if contexto.get("completo", False) else None,
            "historico": self._historico[-5:] if contexto.get("incluir_historico", False) else None
        }
    
    def _esperar_elemento(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Aguarda um elemento aparecer na página."""
        seletor = contexto.get("seletor")
        if not seletor:
            raise ElementoNaoEncontrado("seletor não informado", 0)
        
        timeout = contexto.get("timeout", self._timeout)
        
        try:
            self.page.wait_for_selector(seletor, timeout=timeout)
            return {
                "encontrado": True,
                "seletor": seletor,
                "timeout": timeout
            }
        except PlaywrightTimeoutError:
            raise ElementoNaoEncontrado(seletor, timeout)
    
    def _capturar_tela(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Captura screenshot da página atual."""
        caminho = contexto.get("caminho")
        
        if not caminho:
            identidade_path = Path(self.identidade)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho = str(identidade_path / f"screenshot_{timestamp}.png")
        
        try:
            self.page.screenshot(path=caminho, full_page=contexto.get("completa", False))
            
            return {
                "caminho": caminho,
                "tamanho": Path(caminho).stat().st_size,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise NavegacaoErro("screenshot", str(e))
    
    def _preencher_formulario(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Preenche campos de formulário."""
        campos = contexto.get("campos", {})
        if not campos:
            raise NavegacaoErro("formulário", "Nenhum campo para preencher")
        
        resultados = {}
        for seletor, valor in campos.items():
            try:
                self.page.fill(seletor, valor)
                resultados[seletor] = "preenchido"
            except Exception as e:
                resultados[seletor] = f"erro: {str(e)}"
        
        return {
            "preenchidos": resultados,
            "total": len(campos),
            "sucessos": sum(1 for r in resultados.values() if r == "preenchido")
        }
    
    def _clicar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Clica em um elemento."""
        seletor = contexto.get("seletor")
        if not seletor:
            raise NavegacaoErro("clique", "Seletor não informado")
        
        try:
            self.page.click(seletor)
            return {
                "seletor": seletor,
                "clicado": True,
                "url_apos_clique": self.page.url
            }
        except Exception as e:
            raise NavegacaoErro("clique", str(e))
    
    def _extrair_dados(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados estruturados da página."""
        estrutura = contexto.get("estrutura", {})
        if not estrutura:
            raise NavegacaoErro("extração", "Estrutura de dados não definida")
        
        dados = {}
        for nome, seletor in estrutura.items():
            try:
                elemento = self.page.query_selector(seletor)
                dados[nome] = elemento.inner_text() if elemento else None
            except Exception:
                dados[nome] = None
        
        return {
            "dados": dados,
            "url": self.page.url,
            "timestamp": datetime.now().isoformat()
        }
    
    def _voltar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Volta para página anterior."""
        try:
            self.page.go_back()
            return {
                "url_atual": self.page.url,
                "titulo": self.page.title()
            }
        except Exception as e:
            raise NavegacaoErro("voltar", str(e))
    
    def _recarregar(self, contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Recarrega a página atual."""
        try:
            self.page.reload()
            return {
                "url": self.page.url,
                "titulo": self.page.title()
            }
        except Exception as e:
            raise NavegacaoErro("recarregar", str(e))
    
    # ==================== MÉTODOS PRIVADOS ====================
    
    def _inicializar_navegador(self, contexto: Dict[str, Any]) -> None:
        """Inicializa o navegador com configurações."""
        headless = contexto.get("headless", self._headless)
        identidade = self._identidade or str(Path(self.DIRETORIO_IDENTIDADES) / self._nome.lower())
        
        # Garantir diretório de identidade
        Path(identidade).mkdir(parents=True, exist_ok=True)
        
        self._playwright = sync_playwright().start()
        
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=identidade,
            headless=headless,
            viewport=contexto.get("viewport", {"width": 1280, "height": 720})
        )
        
        # Registrar callback
        self._context.on("close", self._ao_fechar_navegador)
        
        # Abrir página inicial
        paginas = self._context.pages
        self._page = paginas[0] if paginas else self._context.new_page()
        
        # Navegar para URL inicial
        url_inicial = contexto.get("url_inicial", self.URL_INICIAL)
        self._page.goto(url_inicial)
        
        self._registrar_evento(
            evento="navegador_inicializado",
            descricao=f"Navegador inicializado para {self._nome}",
            dados={
                "headless": headless,
                "identidade": identidade,
                "url_inicial": url_inicial
            }
        )
    
    def _ao_fechar_navegador(self) -> None:
        """Callback quando o navegador é fechado."""
        self._registrar_evento(
            evento="navegador_fechado",
            descricao=f"Navegador do Habitante '{self._nome}' foi fechado",
            dados={"ultima_url": self._page.url if self._page else None}
        )
        
        self._page = None
        self._context = None
        self._esta_desperto = False
    
    # ==================== MÉTODOS DE UTILIDADE ====================
    
    def obter_historico(self, limite: Optional[int] = None) -> List[Dict]:
        """Retorna o histórico de navegação."""
        if limite:
            return self._historico[-limite:]
        return self._historico
    
    def limpar_historico(self) -> None:
        """Limpa o histórico de navegação."""
        self._historico = []
    
    def definir_timeout(self, timeout: int) -> None:
        """Define o timeout padrão para navegação."""
        self._timeout = timeout
    
    def obter_status(self) -> Dict[str, Any]:
        """Retorna o status atual do Habitante."""
        return {
            "nome": self._nome,
            "profissao": self.profissao(),
            "esta_desperto": self._esta_desperto,
            "url_atual": self._page.url if self._page else None,
            "historico_count": len(self._historico),
            "ultima_acao": self._ultima_acao,
            "tempo_ativo": str(datetime.now() - self._timestamp_inicio) if self._timestamp_inicio else None
        }