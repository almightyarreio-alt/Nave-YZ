from pydantic import BaseModel, Field


class CifraDespertar(BaseModel):
    """
    Cifra enviada ao Portal para despertar um habitante Navegador.
    """

    nome: str = Field(
        ...,
        min_length=1,
        description="Nome da identidade do habitante Navegador que deve despertar."
    )


class CifraResposta(BaseModel):
    sucesso: bool

    mensagem: str

    habitante: str