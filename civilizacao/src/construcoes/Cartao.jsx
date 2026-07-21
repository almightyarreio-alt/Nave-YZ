export default function Cartao({ titulo, descricao }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
      <h2 className="text-lg font-semibold text-gray-700 mb-2">{titulo}</h2>
      <p className="text-gray-600">{descricao}</p>
    </div>
  )
}