from pydantic import BaseModel, Field


class CifraRegistroCronica(BaseModel):

    origem: dict = Field(
        ...,
        description="Entidade responsável pelo acontecimento."
    )

    evento: str = Field(
        ...,
        description="Nome do acontecimento registrado."
    )

    descricao: str = Field(
        ...,
        description="Descrição humana do acontecimento."
    )

    dados: dict = Field(
        default={},
        description="Informações adicionais do evento."
    )

    nivel: str = Field(
        default="INFO",
        description="Severidade do registro."
    )