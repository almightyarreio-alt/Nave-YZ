from fastapi import APIRouter

portal_teste = APIRouter(prefix="/api")

# ============================================================
# DADOS DE TESTE - Habitantes do Planeta Nave YZ
# ============================================================

perfis = [
    {"id": 1, "nome": "Zara Thorn", "cargo": "Comandante", "setor": "Ponte"},
    {"id": 2, "nome": "Kai Ventura", "cargo": "Piloto", "setor": "Navegação"},
    {"id": 3, "nome": "Luna Eclipse", "cargo": "Engenheira", "setor": "Propulsão"},
    {"id": 4, "nome": "Rex Forge", "cargo": "Mecânico", "setor": "Manutenção"},
    {"id": 5, "nome": "Nova Stellar", "cargo": "Cientista", "setor": "Pesquisa"},
    {"id": 6, "nome": "Orion Black", "cargo": "Oficial Tático", "setor": "Defesa"},
    {"id": 7, "nome": "Iris Vega", "cargo": "Médica", "setor": "Enfermaria"},
    {"id": 8, "nome": "Atlas Storm", "cargo": "Navegador", "setor": "Cartografia"},
    {"id": 9, "nome": "Selene Ash", "cargo": "Comunicadora", "setor": "Transmissões"},
    {"id": 10, "nome": "Phoenix Ember", "cargo": "Estrategista", "setor": "Planejamento"},
]

fluxos = [
    {"id": 1, "nome": "Órbita de Reconhecimento", "status": "ativo", "setor": "Navegação"},
    {"id": 2, "nome": "Varredura de Proximidade", "status": "ativo", "setor": "Sensores"},
    {"id": 3, "nome": "Protocolo de Aterrissagem", "status": "pendente", "setor": "Ponte"},
    {"id": 4, "nome": "Mapeamento Estelar", "status": "ativo", "setor": "Cartografia"},
    {"id": 5, "nome": "Manutenção de Rotina", "status": "concluído", "setor": "Engenharia"},
    {"id": 6, "nome": "Calibragem de Escudos", "status": "ativo", "setor": "Defesa"},
    {"id": 7, "nome": "Coleta de Amostras", "status": "pendente", "setor": "Pesquisa"},
    {"id": 8, "nome": "Transmissão de Dados", "status": "ativo", "setor": "Comunicação"},
    {"id": 9, "nome": "Recarga de Núcleo", "status": "pendente", "setor": "Propulsão"},
    {"id": 10, "nome": "Patrulha de Perímetro", "status": "ativo", "setor": "Segurança"},
]

monitoramentos = [
    {"id": 1, "nome": "Nível de Oxigênio", "valor": "98%", "perfil": 1},
    {"id": 2, "nome": "Temperatura do Núcleo", "valor": "3200K", "perfil": 4},
    {"id": 3, "nome": "Pressurização", "valor": "1.2 atm", "perfil": 4},
    {"id": 4, "nome": "Combustível", "valor": "87%", "perfil": 7},
    {"id": 5, "nome": "Integridade do Casco", "valor": "94%", "perfil": 10},
    {"id": 6, "nome": "Radiação Externa", "valor": "12 mSv", "perfil": 5},
    {"id": 7, "nome": "Campo Gravitacional", "valor": "0.8G", "perfil": 3},
    {"id": 8, "nome": "Sistema Elétrico", "valor": "110%", "perfil": 1},
    {"id": 9, "nome": "Reservas de Água", "valor": "72%", "perfil": 2},
    {"id": 10, "nome": "Comunicação Interplanetária", "valor": "Online", "perfil": 1},
]


# ============================================================
# ENDPOINTS
# ============================================================

@portal_teste.get("/saudacao")
def saudacao():
    return {
        "mensagem": "Bem-vindo ao Nave YZ!"
    }

@portal_teste.get("/perfis")
def listar_perfis():
    return {"habitantes": "perfis", "dados": perfis}


@portal_teste.get("/perfis/{perfil_id}")
def obter_perfil(perfil_id: int):
    for perfil in perfis:
        if perfil["id"] == perfil_id:
            return {"habitante": "perfil", "dados": perfil}
    return {"erro": "Perfil não encontrado"}


@portal_teste.get("/fluxos")
def listar_fluxos():
    return {"habitantes": "fluxos", "dados": fluxos}


@portal_teste.get("/fluxos/{fluxo_id}")
def obter_fluxo(fluxo_id: int):
    for fluxo in fluxos:
        if fluxo["id"] == fluxo_id:
            return {"habitante": "fluxo", "dados": fluxo}
    return {"erro": "Fluxo não encontrado"}


@portal_teste.get("/monitoramentos")
def listar_monitoramentos():
    return {"habitantes": "monitoramentos", "dados": monitoramentos}


@portal_teste.get("/monitoramentos/{monitoramento_id}")
def obter_monitoramento(monitoramento_id: int):
    for mon in monitoramentos:
        if mon["id"] == monitoramento_id:
            return {"habitante": "monitoramento", "dados": mon}
    return {"erro": "Monitoramento não encontrado"}

@portal_teste.get("/monitoramento/perfil/{perfil_id}")
def listar_monitoramentos_por_perfil(perfil_id: int):
    """
    Retorna monitoramento filtrados diretamenbte pelo campo 'pefil'.
    """
    # Busca o perfil para incluir na resposta

    perfil = None 
    for p in perfis :
        if p["id"] == perfil_id:

            perfil = p

            break
    
    if not perfil:
        return {"erro": "Perfil não encontrado"}
    
    monitoramentos_filtrados = [
        mon for mon in monitoramentos if mon["perfil"] == perfil_id
    ]

    
    return {
        "habitante": "monitoramento_por_perfil",
        "perfil" : perfil,
        "total" : len(monitoramentos_filtrados),
        "dados": monitoramentos_filtrados}


@portal_teste.post("/executar/fluxo/{perfil_id}/{fluxo_id}")
def executar_fluxo(perfil_id: int, fluxo_id: int):
    """
    Simula a execução de um fluxo em um perfil.
    Retorna os monitoramentos atualizados após a execução.
    """
    # Busca o perfil
    perfil = next((p for p in perfis if p["id"] == perfil_id), None)
    if not perfil:
        return {"erro": "Perfil não encontrado"}
    
    # Busca o fluxo
    fluxo = next((f for f in fluxos if f["id"] == fluxo_id), None)
    if not fluxo:
        return {"erro": "Fluxo não encontrado"}
    
    # Monitoramentos do perfil
    monitoramentos_do_perfil = [
        mon for mon in monitoramentos if mon["perfil"] == perfil_id
    ]
    
    # Simula a execução: altera valores aleatoriamente
    import random
    novos_valores = ["normal", "atenção", "crítico", "sobrecarga"]
    
    resultado = []
    for mon in monitoramentos_do_perfil:
        mon_executado = mon.copy()
        mon_executado["alerta"] = random.choice(novos_valores)
        resultado.append(mon_executado)
    
    return {
        "habitante": "execucao",
        "fluxo": fluxo,
        "perfil": perfil,
        "mensagem": f"Fluxo '{fluxo['nome']}' executado em {perfil['nome']}",
        "dados": resultado
    }