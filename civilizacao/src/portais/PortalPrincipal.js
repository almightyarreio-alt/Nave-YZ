import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000', // seu servidor FastAPI
})

export const buscarSaudacao = async () => {
  const response = await api.get('/api/saudacao')  
  
  return response.data.mensagem
}

export const buscarPerfis = async () => {
  const response = await api.get("/api/perfis");
  return response.data.dados;
};

export const buscarFluxos = async () => {
  const response = await api.get("/api/fluxos");
  return response.data.dados;
};

export const buscarMonitoramentos = async () => {
  const response = await api.get("/api/monitoramentos");
  return response.data.dados;
};

// Monitoramentos por perfil
export const buscarMonitoramentosPorPerfil = async (perfilId) => {
  const response = await api.get(`/api/monitoramento/perfil/${perfilId}`);
  return response.data;
};

// Executar fluxo no perfil
export const executarFluxo = async (perfilId, fluxoId) => {
  const response = await api.post(`/api/executar/fluxo/${perfilId}/${fluxoId}`);
  return response.data;
};