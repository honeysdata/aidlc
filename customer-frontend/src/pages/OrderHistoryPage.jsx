import { useState, useEffect, useCallback } from 'react'
import { Layout } from '../components/layout/Layout'
import { OrderItem } from '../components/order/OrderItem'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { customerApi } from '../api/client'
import { useSSE } from '../hooks/useSSE'
import './OrderHistoryPage.css'

export function OrderHistoryPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const loadOrders = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await customerApi.getOrders()
      setOrders(response.data.orders)
    } catch (err) {
      setError('주문 내역을 불러오는데 실패했습니다')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOrders()
  }, [])

  // SSE 이벤트 핸들러
  const handleSSEEvent = useCallback((event) => {
    if (event.type === 'order_updated') {
      setOrders((prev) =>
        prev.map((order) =>
          order.id === event.data.order_id
            ? { ...order, status: event.data.status }
            : order
        )
      )
    } else if (event.type === 'order_deleted') {
      setOrders((prev) =>
        prev.filter((order) => order.id !== event.data.order_id)
      )
    }
  }, [])

  useSSE(handleSSEEvent)

  if (loading) {
    return (
      <Layout>
        <Loading message="주문 내역을 불러오는 중..." />
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout>
        <ErrorMessage message={error} onRetry={loadOrders} />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="order-history-page">
        <h2>주문 내역</h2>
        
        {orders.length === 0 ? (
          <div className="order-empty">
            <span className="order-empty-icon">📋</span>
            <p>주문 내역이 없습니다</p>
          </div>
        ) : (
          <div className="order-list">
            {orders.map((order) => (
              <OrderItem key={order.id} order={order} />
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
