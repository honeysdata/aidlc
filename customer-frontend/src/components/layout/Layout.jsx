import { Header } from './Header'
import { Navigation } from './Navigation'
import './Layout.css'

export function Layout({ children, showNav = true }) {
  return (
    <div className="layout">
      <Header />
      <main className="main-content">{children}</main>
      {showNav && <Navigation />}
    </div>
  )
}
