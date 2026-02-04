import { formatPrice } from '../../utils/format'
import { useCart } from '../../contexts/CartContext'
import './MenuCard.css'

export function MenuCard({ menu }) {
  const { addItem } = useCart()

  const handleAdd = () => {
    addItem(menu)
  }

  return (
    <div className="menu-card">
      <div className="menu-info">
        <h3 className="menu-name">{menu.name}</h3>
        {menu.description && (
          <p className="menu-description">{menu.description}</p>
        )}
        <p className="menu-price">{formatPrice(menu.price)}</p>
      </div>
      <button className="menu-add-btn" onClick={handleAdd}>
        +
      </button>
    </div>
  )
}
