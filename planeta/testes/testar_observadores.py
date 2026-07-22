"""
🧪 Teste dos Observadores

Valida:

Observador
Sinal
Cronista
"""


from planeta.observadores.sinais import Sinal
from planeta.observadores.cronista import Cronista



def testar_cronista():


    print("\n👁 TESTANDO CRONISTA")


    cronista = Cronista()


    cronista.ativar()


    sinal = Sinal(

        tipo="PLANETA_DESPERTOU",

        origem="Nave YZ",

        dados={

            "estado": "ativo"

        }

    )


    registro = cronista.observar(
        sinal
    )


    print(registro)


    assert cronista.estado == "ativo"


    assert len(
        cronista.historico()
    ) == 1



if __name__ == "__main__":

    testar_cronista()


    print(
        """
==============================

✅ OBSERVADOR FUNCIONANDO

==============================
"""
    )