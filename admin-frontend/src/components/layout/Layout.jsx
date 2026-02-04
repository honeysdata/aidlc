import { NavLink } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import './Layout.css'

export function Layout({ children }) {
  const { user, logout } = useAuth()

  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>테이블 오더</h1>
          <span className="store-name">{user?.storeId}</span>
        </div>
        
        <nav className="sidebar-nav">
          <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} end>
            📊 대시보드
          </NavLink>
          <NavLink to="/tables" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            🪑 테이블 관리
          </NavLink>
          <NavLink to="/menus" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            🍽️ 메뉴 관리
          </NavLink>
          <NavLink to="/categories" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            📁 카테고리 관리
          </NavLink>
        </nav>
        
        <div className="sidebar-footer">
          <span className="user-name">{user?.username}</span>
          <button className="logout-btn" onClick={logout}>로그아웃</button>
        </div>
      </aside>
      
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}
