import { useEffect, useState } from "react";
import { buscarMonitoramentos } from "../portais/PortalPrincipal";
import Tabela from "../construcoes/Tabela";

export default function Monitoramentos() {
  const [monitoramentos, setMonitoramentos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    buscarMonitoramentos()
      .then((dados) => setMonitoramentos(dados))
      .finally(() => setCarregando(false));
  }, []);

  // Definição das colunas da tabela
  const colunas = [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "valor", titulo: "Valor" },
    { chave: "perfil", titulo: "Perfil" },
  ];

  return (
    <div className="p-8 space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Monitoramentos</h1>
          <p className="text-gray-400 mt-1">Monitoramentos da Nave YZ</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800/50 border border-gray-700/50">
          <span className="w-2 h-2 rounded-full bg-cyan-400" />
          <span className="text-sm text-gray-300">
            {carregando ? "Carregando..." : `${monitoramentos.length} monitoramentos`}
          </span>
        </div>
      </div>

      {/* Tabela de Monitoramentos */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 overflow-hidden">
        {carregando ? (
          <div className="p-12 text-center text-gray-400">
            <div className="inline-block w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-2" />
            <p>Carregando monitoramentos...</p>
          </div>
        ) : (
          <Tabela colunas={colunas} dados={monitoramentos} />
        )}
      </div>
    </div>
  );
}