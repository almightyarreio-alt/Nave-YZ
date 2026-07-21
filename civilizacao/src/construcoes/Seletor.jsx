export default function Seletor({ label, valor, onChange, opcoes, placeholder }) {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider">
          {label}
        </label>
      )}
      <select
        value={valor}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-2.5 bg-gray-800/80 border border-gray-700/50 rounded-lg text-gray-200 
                   focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30
                   appearance-none cursor-pointer
                   bg-[url('data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2212%22%20height%3D%2212%22%20viewBox%3D%220%200%2012%2012%22%3E%3Cpath%20fill%3D%22%239ca3af%22%20d%3D%22M6%208L1%203h10z%22%2F%3E%3C%2Fsvg%3E')] 
                   bg-[length:12px] bg-[right_12px_center] bg-no-repeat"
      >
        <option value="">{placeholder || "Selecione..."}</option>
        {opcoes.map((opcao) => (
          <option key={opcao.valor} value={opcao.valor}>
            {opcao.rotulo}
          </option>
        ))}
      </select>
    </div>
  );
}