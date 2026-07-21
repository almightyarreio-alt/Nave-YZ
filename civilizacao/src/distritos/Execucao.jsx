import { useEffect, useState } from "react";
import { 
  buscarPerfis, 
  buscarFluxos, 
  buscarMonitoramentosPorPerfil, 
  executarFluxo 
} from "../portais/PortalPrincipal";
import Seletor from "../construcoes/Seletor";
import Tabela from "../construcoes/Tabela";

export default function Execucao() {
  // Estados
  const [perfis, setPerfis] = useState([]);
  const [fluxos, setFluxos] = useState([]);
  const [monitoramentos, setMonitoramentos] = useState([]);
  
  const [perfilSelecionado, setPerfilSelecionado] = useState("");
  const [fluxoSelecionado, setFluxoSelecionado] = useState("");
  
  const [carregando, setCarregando] = useState(false);
  const [executando, setExecutando] = useState(false);
  const [mensagemExecucao, setMensagemExecucao] = useState("");

  // Carrega perfis e fluxos ao montar
  useEffect(() => {
    buscarPerfis().then(setPerfis);
    buscarFluxos().then(setFluxos);
  }, []);

  // Quando um perfil é selecionado, busca os monitoramentos
  useEffect(() => {
    if (!perfilSelecionado) {
      setMonitoramentos([]);
      return;
    }
    
    setCarregando(true);
    setMensagemExecucao("");
    buscarMonitoramentosPorPerfil(perfilSelecionado)
      .then((res) =>{
            
         setMonitoramentos(res.dados)})
        
      .finally(() => setCarregando(false));
  }, [perfilSelecionado]);

  // Executar fluxo
  const handleExecutar = async () => {
    if (!perfilSelecionado || !fluxoSelecionado) return;
    
    setExecutando(true);
    setMensagemExecucao("");
    
    try {
      const resultado = await executarFluxo(perfilSelecionado, fluxoSelecionado);
      setMonitoramentos(resultado.dados);
      setMensagemExecucao(resultado.mensagem);
    } catch (erro) {
      setMensagemExecucao("Erro ao executar fluxo");
    } finally {
      setExecutando(false);
    }
  };

  // Colunas da tabela
  const colunas = [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Monitoramento" },
    { chave: "valor", titulo: "Valor" },
    { 
      chave: "alerta", 
      titulo: "Status",
      render: (valor) => {
        const cores = {
          normal: "bg-green-400/10 text-green-400 border-green-400/20",
          atenção: "bg-yellow-400/10 text-yellow-400 border-yellow-400/20",
          crítico: "bg-red-400/10 text-red-400 border-red-400/20",
          sobrecarga: "bg-orange-400/10 text-orange-400 border-orange-400/20",
        };
        return (
          <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${cores[valor] || "bg-gray-400/10 text-gray-400 border-gray-400/20"}`}>
            {valor}
          </span>
        );
      }
    },
    { chave: "perfil", titulo: "Perfil ID" },
  ];

  return (
    <div className="p-8 space-y-6">
      {/* Cabeçalho */}
      <div>
        <h1 className="text-3xl font-bold text-white">Monitoramentos</h1>
        <p className="text-gray-400 mt-1">Execute fluxos e visualize monitoramentos por perfil</p>
      </div>

      {/* Seletores e Execução */}
      <div className="bg-gray-800/30 backdrop-blur-sm rounded-xl border border-gray-700/50 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <Seletor
            label="Perfil"
            placeholder="Selecione um tripulante..."
            valor={perfilSelecionado}
            onChange={(valor) => {
              setPerfilSelecionado(valor);
              setFluxoSelecionado("");
            }}
            opcoes={perfis.map(p => ({
              valor: p.id,
              rotulo: `${p.nome} — ${p.cargo} (${p.setor})`
            }))}
          />
          
          <Seletor
            label="Fluxo"
            valor={fluxoSelecionado}
            onChange={setFluxoSelecionado}          
            opcoes={fluxos.map(f => ({
              valor: f.id,
              rotulo: `${f.nome} [${f.status}]`
            }))}
            placeholder="Selecione um fluxo para executar..."
          />
        </div>

        {/* Botão Executar */}
        <button
          onClick={handleExecutar}
          disabled={!perfilSelecionado || !fluxoSelecionado || executando}
          className={`w-full py-3 px-6 rounded-lg font-medium text-sm transition-all duration-200 
            ${!perfilSelecionado || !fluxoSelecionado
              ? "bg-gray-700/50 text-gray-500 cursor-not-allowed"
              : "bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:from-cyan-400 hover:to-blue-500 shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 active:scale-[0.98]"
            }`}
        >
          {executando ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Executando...
            </span>
          ) : (
            "Executar Fluxo"
          )}
        </button>

        {/* Mensagem de execução */}
        {mensagemExecucao && (
          <div className="mt-4 p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-lg">
            <p className="text-cyan-300 text-sm">{mensagemExecucao}</p>
          </div>
        )}
      </div>

      {/* Tabela de Monitoramentos */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 overflow-hidden">
        {!perfilSelecionado ? (
          <div className="p-12 text-center text-gray-500">
            <svg className="w-12 h-12 mx-auto mb-3 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p>Selecione um perfil para visualizar os monitoramentos</p>
          </div>
        ) : carregando ? (
          <div className="p-12 text-center text-gray-400">
            <div className="inline-block w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-2" />
            <p>Carregando monitoramentos...</p>
          </div>
        ) : monitoramentos.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <p>Nenhum monitoramento encontrado para este perfil</p>
          </div>
        ) : (
          <Tabela 
             colunas={colunas.map(c => ({ chave: c.chave, titulo: c.titulo }))}
             dados={monitoramentos}
            colunasComRender={colunas}            
          />
        )}
      </div>
    </div>
  );
}