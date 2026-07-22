from planeta.planeta import Planeta


nave_yz = Planeta(
    nome="Nave YZ",
    tipo="Planeta de Automação Inteligente",
    proposito=(
        "Executar fluxos automatizados "
        "entre humanos e máquinas."
    ),
    constelacao="Automação"
)


nave_yz.despertar()


print(
    nave_yz.diagnostico()
)