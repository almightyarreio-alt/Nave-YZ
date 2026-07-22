from fastapi import APIRouter
from planeta.cifras.cifra_navegacao import (CifraDespertar, CifraResposta)
from planeta.habitantes.navegador import (habitante_navegador)

portal = APIRouter(
    prefix="/portal/navegacao",
    tags=["Navegação"]
)


@portal.post(
    "/despertar",
    response_model=CifraResposta,
    summary = "Despertar Habitante Navegador",
    description= "Endpoint para despertar o Habitante Navegador do Planeta Nave YZ."
)

def despertar(cifra: CifraDespertar):

    return habitante_navegador.despertar(cifra.nome)