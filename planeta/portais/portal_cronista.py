from fastapi import APIRouter

from cifras.cifra_cronista import (
    CifraRegistroCronica
)

from observadores.cronista import cronista


portal = APIRouter(
    prefix="/portal/cronista",
    tags=["Cronista"]
)


@portal.post("/registrar")
def registrar(cifra: CifraRegistroCronica):

    registro = cronista.registrar(

        origem=cifra.origem,

        evento=cifra.evento,

        descricao=cifra.descricao,

        dados=cifra.dados,

        nivel=cifra.nivel
    )


    return {
        "sucesso": True,
        "registro": registro
    }