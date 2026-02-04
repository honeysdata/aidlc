import { useNavigate } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { CartItem } from '../components/cart/CartItem'
import { CartSummary } from '../components/cart/CartSummary'
import { Button } from '../components/common/Button'
import { useCart } from '../contexts/CartContext'
import './CartPage.css'

export function CartPage() {
  const { items, totalQuantity, totalAmount, clearCart } = useCart()
  const navigate = useNavigate()

  const handleOrder = () => {
    navigate('/order/confirm')
  }

  if (items.length === 0) {
    return (
      <Layout>
        <div className="cart-empty">
          <span className="cart-empty-icon">🛒</span>
          <p>장바구니가 비어있습니다</p>
          <Button variant="primary" onClick={() => navigate('/menu')}>
            메뉴 보러가기
          </Button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="cart-page">
        <div className="cart-header">
          <h2>장바구니</h2>
          <button className="cart-clear-btn" onClick={clearCart}>
            전체 삭제
          </button>
        </div>
        
        <div className="cart-items">
          {items.map((item) => (
            <CartItem key={item.id} item={item} />
          ))}
        </div>
        
        <CartSummary totalQuantity={totalQuantity} totalAmount={totalAmount} />
        
        <div className="cart-actions">
          <Button size="large" onClick={handleOrder}>
            주문하기
          </Button>
        </div>
      </div>
    </Layout>
  )
}
