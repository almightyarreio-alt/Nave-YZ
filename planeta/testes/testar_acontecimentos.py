"""
🧪 Teste do Sistema de Acontecimentos

Valida o núcleo histórico do Planeta:

- Catálogo oficial
- Categorias
- Severidades
- Fabricação
- Acontecimentos
- Crônicas
"""

from planeta.acontecimentos.catalogo import Catalogo
from planeta.acontecimentos.fabrica import fabrica
from planeta.acontecimentos.cronica import Cronica


def testar_catalogo():

    print("\n📚 TESTANDO CATÁLOGO")

    acontecimentos = Catalogo.todos()

    assert len(acontecimentos) > 0

    for item in acontecimentos:

        print(
            f"""
Evento:
  Código: {item.codigo}
  Categoria: {item.categoria.value}
  Severidade: {item.severidade.value}
  Descrição: {item.descricao}
"""
        )



def testar_fabrica():

    print("\n🏭 TESTANDO FÁBRICA")

    acontecimento = fabrica.criar(

        definicao=Catalogo.PLANETA_DESPERTOU,

        origem={
            "tipo": "Planeta",
            "nome": "Nave YZ"
        },

        contexto={
            "estado": "ativo"
        }
    )


    assert acontecimento.codigo == "planeta_despertou"


    print(
        acontecimento.to_dict()
    )



def testar_cronica():

    print("\n📜 TESTANDO CRÔNICA")


    acontecimento = fabrica.criar(

        definicao=Catalogo.HABITANTE_CRIADO,

        origem={
            "tipo": "Habitante",
            "nome": "Cronista"
        },

        dados={
            "missao": "Registrar história"
        }
    )


    cronica = Cronica(
        acontecimento=acontecimento
    )


    documento = cronica.to_dict()


    assert documento["acontecimento"]["codigo"] == (
        "habitante_criado"
    )


    print(documento)



def testar_categorias():

    print("\n🏷 TESTANDO CATEGORIAS")

    evento = Catalogo.PORTAL_ABERTO


    assert evento.categoria.value == (
        "portal"
    )


    print(
        evento.categoria
    )



def testar_severidades():

    print("\n🚨 TESTANDO SEVERIDADES")

    evento = Catalogo.FALHA_CRITICA


    assert evento.severidade.value == (
        "critico"
    )


    print(
        evento.severidade
    )



if __name__ == "__main__":

    testar_catalogo()

    testar_fabrica()

    testar_cronica()

    testar_categorias()

    testar_severidades()


    print(
        """
================================

✅ TODOS OS TESTES PASSARAM

O sistema de acontecimentos
está consistente.

================================
"""
    )