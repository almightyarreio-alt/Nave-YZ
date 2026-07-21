import { useEffect, useState } from "react";
import { buscarSaudacao } from "../portais/PortalPrincipal";

export default function Painel() {
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    buscarSaudacao().then(setMensagem);
  }, []);

  return (
    <div className="p-8 space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Painel de Comando</h1>
          <p className="text-gray-400 mt-1">Visão geral da Nave YZ</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800/50 border border-gray-700/50">
          <span className="w-2 h-2 rounded-full bg-green-400" />
          <span className="text-sm text-gray-300">Todos os sistemas operacionais</span>
        </div>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Card de Boas-vindas */}
        <div className="col-span-full bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 22h20L12 2zm0 4l6 14H6l6-14z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Boas-vindas</h2>
              <p className="text-gray-400 mt-1">{mensagem || "Carregando transmissão..."}</p>
            </div>
          </div>
        </div>

        {/* Cards de exemplo para o Dashboard */}
        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50">
          <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider">Perfis</h3>
          <p className="text-3xl font-bold text-white mt-2">10</p>
          <p className="text-sm text-cyan-400 mt-1">Tripulantes ativos</p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50">
          <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider">Fluxos</h3>
          <p className="text-3xl font-bold text-white mt-2">10</p>
          <p className="text-sm text-yellow-400 mt-1">3 pendentes</p>
        </div>

        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50">
          <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider">Monitoramentos</h3>
          <p className="text-3xl font-bold text-white mt-2">10</p>
          <p className="text-sm text-red-400 mt-1">2 alertas</p>
        </div>
      </div>
    </div>
  );
}