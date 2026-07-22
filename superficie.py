from fastapi import FastAPI

from planeta.planeta import Planeta


nave_yz = Planeta(nome="Nave YZ")

nave_yz.despertar()


superficie = FastAPI(title="Nave YZ")


@superficie.get("/")
def entrada():

    return {
        "planeta": nave_yz.nome,
        "estado": nave_yz.estado
    }