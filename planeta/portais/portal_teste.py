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
    {"id": 1, "nome": "Nível de Oxigênio", "valor": "98%", "alerta": "normal"},
    {"id": 2, "nome": "Temperatura do Núcleo", "valor": "3200K", "alerta": "atenção"},
    {"id": 3, "nome": "Pressurização", "valor": "1.2 atm", "alerta": "normal"},
    {"id": 4, "nome": "Combustível", "valor": "87%", "alerta": "normal"},
    {"id": 5, "nome": "Integridade do Casco", "valor": "94%", "alerta": "normal"},
    {"id": 6, "nome": "Radiação Externa", "valor": "12 mSv", "alerta": "crítico"},
    {"id": 7, "nome": "Campo Gravitacional", "valor": "0.8G", "alerta": "normal"},
    {"id": 8, "nome": "Sistema Elétrico", "valor": "110%", "alerta": "sobrecarga"},
    {"id": 9, "nome": "Reservas de Água", "valor": "72%", "alerta": "atenção"},
    {"id": 10, "nome": "Comunicação Interplanetária", "valor": "Online", "alerta": "normal"},
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