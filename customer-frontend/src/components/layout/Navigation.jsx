import { NavLink } from 'react-router-dom'
import { useCart } from '../../contexts/CartContext'
import './Navigation.css'

export function Navigation() {
  const { totalQuantity } = useCart()

  return (
    <nav className="navigation">
      <NavLink to="/menu" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <span className="nav-icon">🍽️</span>
        <span className="nav-label">메뉴</span>
      </NavLink>
      
      <NavLink to="/cart" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <span className="nav-icon">
          🛒
          {totalQuantity > 0 && (
            <span className="nav-badge">{totalQuantity}</span>
          )}
        </span>
        <span className="nav-label">장바구니</span>
      </NavLink>
      
      <NavLink to="/orders" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <span className="nav-icon">📋</span>
        <span className="nav-label">주문내역</span>
      </NavLink>
    </nav>
  )
}
