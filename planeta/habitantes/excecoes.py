class HabitanteErro(Exception):
    """Erro base para Habitantes."""
    pass

class HabitanteAdormecido(HabitanteErro):
    """Lançada quando um Habitante adormecido é chamado."""
    def __init__(self, nome: str):
        super().__init__(f"O Habitante '{nome}' está adormecido.")
        self.nome = nome

class ViolacaoLeis(HabitanteErro):
    """Lançada quando uma ação viola as Leis."""
    def __init__(self, acao: str, motivo: str):
        super().__init__(f"Ação '{acao}' viola as Leis: {motivo}")
        self.acao = acao
        self.motivo = motivo

class NavegacaoErro(HabitanteErro):
    """Lançada quando ocorre um erro de navegação."""
    def __init__(self, destino: str, motivo: str):
        super().__init__(f"Erro ao navegar para '{destino}': {motivo}")
        self.destino = destino

class ElementoNaoEncontrado(HabitanteErro):
    """Lançada quando um elemento não é encontrado."""
    def __init__(self, seletor: str, timeout: int):
        super().__init__(f"Elemento '{seletor}' não encontrado após {timeout}ms")
        self.seletor = seletor
        self.timeout = timeout

class AcaoInvalida(HabitanteErro):
    """Lançada quando uma ação inválida é solicitada."""
    def __init__(self, acao: str, validas: list):
        super().__init__(f"Ação '{acao}' inválida. Ações válidas: {', '.join(validas)}")
        self.acao = acao
        self.validas = validas