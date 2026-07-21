import { NavLink } from "react-router-dom";

const links = [
  {
    to: "/",
    label: "Painel",
    icone: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    ),
  },
  {
    to: "/perfis",
    label: "Perfis",
    icone: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
  {
    to: "/fluxos",
    label: "Fluxos",
    icone: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
  },
  {
    to: "/monitoramentos",
    label: "Monitoramentos",
    icone: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    to: "/execucoes",
    label: "Execuções",
    icone: (
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-play-icon lucide-play">
        <path d="M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z"/>
        </svg>
    ),
  },
];

export default function BarraLateral() {
  return (
    <nav className="h-full flex flex-col bg-[#0a0e17] border-r border-gray-800">
      {/* Navegação */}
      <div className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        <p className="px-3 mb-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Navegação
        </p>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? "bg-gradient-to-r from-cyan-500/10 to-blue-500/10 text-cyan-400 border border-cyan-500/20 shadow-lg shadow-cyan-500/5"
                  : "text-gray-400 hover:text-gray-200 hover:bg-gray-800/50"
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span className={isActive ? "text-cyan-400" : "text-gray-500 group-hover:text-gray-300 transition-colors"}>
                  {link.icone}
                </span>
                <span>{link.label}</span>
                {isActive && (
                  <span className="ml-auto w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400/50" />
                )}
              </>
            )}
          </NavLink>
        ))}
      </div>

      {/* Status do Sistema (rodapé da sidebar) */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-gray-800/30">
          <div className="w-2 h-2 rounded-full bg-green-400 shadow-sm shadow-green-400/50 animate-pulse" />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-gray-400 truncate">Sistema</p>
            <p className="text-xs text-green-400 font-medium">Online</p>
          </div>
        </div>
      </div>
    </nav>
  );
}