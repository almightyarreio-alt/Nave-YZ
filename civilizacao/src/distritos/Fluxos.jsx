import { useEffect, useState } from "react";
import { buscarFluxos } from "../portais/PortalPrincipal";
import Tabela from "../construcoes/Tabela";

export default function Fluxos() {
  const [fluxos, setFluxos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    buscarFluxos()
      .then((dados) => setFluxos(dados))
      .finally(() => setCarregando(false));
  }, []);

  // Definição das colunas da tabela
  const colunas = [
    { chave: "id", titulo: "ID" },
    { chave: "nome", titulo: "Nome" },
    { chave: "status", titulo: "Status" },
    { chave: "setor", titulo: "Setor" },
  ];

  return (
    <div className="p-8 space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Fluxos</h1>
          <p className="text-gray-400 mt-1">Fluxos automáticos da Nave YZ</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800/50 border border-gray-700/50">
          <span className="w-2 h-2 rounded-full bg-cyan-400" />
          <span className="text-sm text-gray-300">
            {carregando ? "Carregando..." : `${fluxos.length} fluxos`}
          </span>
        </div>
      </div>

      {/* Tabela de Fluxos */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 overflow-hidden">
        {carregando ? (
          <div className="p-12 text-center text-gray-400">
            <div className="inline-block w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-2" />
            <p>Carregando fluxos...</p>
          </div>
        ) : (
          <Tabela colunas={colunas} dados={fluxos} />
        )}
      </div>
    </div>
  );
}