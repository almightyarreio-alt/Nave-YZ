export default function Tabela({ colunas, dados }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-700/50">
            {colunas.map((coluna) => (
              <th
                key={coluna.chave}
                className="text-left px-6 py-4 text-xs font-semibold text-gray-400 uppercase tracking-wider"
              >
                {coluna.titulo}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700/30">
          {dados.map((item) => (
            <tr
              key={item.id}
              className="hover:bg-gray-700/20 transition-colors"
            >
              {colunas.map((coluna) => (
                <td
                  key={coluna.chave}
                  className="px-6 py-4 text-sm text-gray-300 whitespace-nowrap"
                >
                  {item[coluna.chave]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}