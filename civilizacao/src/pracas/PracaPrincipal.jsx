import { Outlet } from 'react-router-dom'
import TemplateDashboard from '../arquitetura/TemplateDashboard'
import BarraLateral from '../construcoes/BarraLateral'

export default function PracaPrincipal() {
  return (
    <TemplateDashboard
      sidebar={<BarraLateral />}
    >
      <Outlet />   {/* Distritos serão exibidos aqui */}
    </TemplateDashboard>
  )
}