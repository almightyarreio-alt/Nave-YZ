import { BrowserRouter, Routes, Route } from 'react-router-dom'
import PracaPrincipal from './pracas/PracaPrincipal'
import Painel from './distritos/Painel'
import Perfis from './distritos/Perfis'
import Fluxos from './distritos/Fluxos'
import Monitoramentos from './distritos/Monitoramento'
import Execucao from './distritos/Execucao'


//import TemplateDashboard from './arquitetura/TemplateDashborad'
// ... outros distritos

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PracaPrincipal />}>
          <Route path="/" element={<Painel />} />
          <Route path="/perfis" element={<Perfis />} />
          <Route path="/fluxos" element={<Fluxos />} />
          <Route path="/monitoramentos" element={<Monitoramentos />} />
          <Route path="/execucoes" element={<Execucao />} />
          {/* futuros Distritos */}
        </Route>
      </Routes>
    </BrowserRouter>
  )
}