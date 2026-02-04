import { useAuth } from '../../contexts/AuthContext'
import './Header.css'

export function Header() {
  const { auth } = useAuth()

  return (
    <header className="header">
      <h1 className="header-title">테이블 오더</h1>
      {auth && (
        <span className="header-table">테이블 {auth.tableNumber}</span>
      )}
    </header>
  )
}
