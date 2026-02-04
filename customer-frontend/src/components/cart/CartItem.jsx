import { formatPrice } from '../../utils/format'
import { useCart } from '../../contexts/CartContext'
import './CartItem.css'

export function CartItem({ item }) {
  const { increaseQuantity, decreaseQuantity, removeItem } = useCart()

  return (
    <div className="cart-item">
      <div className="cart-item-info">
        <h3 className="cart-item-name">{item.name}</h3>
        <p className="cart-item-price">{formatPrice(item.price)}</p>
      </div>
      
      <div className="cart-item-controls">
        <button
          className="cart-qty-btn"
          onClick={() => decreaseQuantity(item.id)}
        >
          −
        </button>
        <span className="cart-qty">{item.quantity}</span>
        <button
          className="cart-qty-btn"
          onClick={() => increaseQuantity(item.id)}
        >
          +
        </button>
      </div>
      
      <div className="cart-item-subtotal">
        {formatPrice(item.price * item.quantity)}
      </div>
      
      <button
        className="cart-remove-btn"
        onClick={() => removeItem(item.id)}
      >
        ✕
      </button>
    </div>
  )
}
