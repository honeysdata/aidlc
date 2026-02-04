import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { CartSummary } from '../components/cart/CartSummary'
import { Button } from '../components/common/Button'
import { useCart } from '../contexts/CartContext'
import { customerApi } from '../api/client'
import { formatPrice } from '../utils/format'
import './OrderConfirmPage.css'

export function OrderConfirmPage() {
  const { items, totalQuantity, totalAmount, clearCart } = useCart()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleConfirm = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const orderData = {
        items: items.map((item) => ({
          menu_id: item.id,
          quantity: item.quantity,
        })),
      }
      
      const response = await customerApi.createOrder(orderData)
      clearCart()
      navigate('/order/success', { 
        state: { orderNumber: response.data.order_number } 
      })
    } catch (err) {
      setError(err.response?.data?.error?.message || '주문에 실패했습니다')
    } finally {
      setLoading(false)
    }
  }

  if (items.length === 0) {
    navigate('/cart')
    return null
  }

  return (
    <Layout showNav={false}>
      <div className="order-confirm-page">
        <h2>주문 확인</h2>
        
        <div className="order-items">
          {items.map((item) => (
            <div key={item.id} className="order-item">
              <span className="order-item-name">{item.name}</span>
              <span className="order-item-qty">x {item.quantity}</span>
              <span className="order-item-price">
                {formatPrice(item.price * item.quantity)}
              </span>
            </div>
          ))}
        </div>
        
        <CartSummary totalQuantity={totalQuantity} totalAmount={totalAmount} />
        
        {error && <p className="order-error">{error}</p>}
        
        <div className="order-actions">
          <Button 
            variant="secondary" 
            size="large" 
            onClick={() => navigate('/cart')}
            disabled={loading}
          >
            돌아가기
          </Button>
          <Button 
            size="large" 
            onClick={handleConfirm}
            loading={loading}
          >
            주문 확정
          </Button>
        </div>
      </div>
    </Layout>
  )
}
