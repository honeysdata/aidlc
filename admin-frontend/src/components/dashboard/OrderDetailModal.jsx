import { useState, useEffect } from 'react'
import { Modal } from '../common/Modal'
import { Button } from '../common/Button'
import { Loading } from '../common/Loading'
import { formatPrice, formatDateTime, formatOrderStatus, getStatusColor } from '../../utils/format'
import { adminApi } from '../../api/client'
import './OrderDetailModal.css'

export function OrderDetailModal({ isOpen, onClose, table, onOrderUpdate, onOrderDelete }) {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isOpen && table?.session_id) {
      loadOrders()
    }
  }, [isOpen, table?.session_id])

  const loadOrders = async () => {
    if (!table?.session_id) return
    
    setLoading(true)
    try {
      const response = await adminApi.getOrdersBySession(table.session_id)
      setOrders(response.data.orders)
    } catch (err) {
      console.error('Failed to load orders:', err)
      setOrders([])
    } finally {
      setLoading(false)
    }
  }

  const handleStatusChange = async (orderId, currentStatus) => {
    const nextStatus = currentStatus === 'pending' ? 'preparing' : 'completed'
    
    try {
      await adminApi.updateOrderStatus(orderId, nextStatus)
      onOrderUpdate(orderId, nextStatus)
      loadOrders()
    } catch (err) {
      alert(err.response?.data?.error?.message || '상태 변경에 실패했습니다')
    }
  }

  const handleDelete = async (orderId) => {
    if (!confirm('정말 이 주문을 삭제하시겠습니까?')) return
    
    try {
      await adminApi.deleteOrder(orderId)
      onOrderDelete(orderId)
    } catch (err) {
      alert(err.response?.data?.error?.message || '삭제에 실패했습니다')
    }
  }

  if (!table) return null

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`테이블 ${table.table_number} 주문 상세`}>
      <div className="order-detail-content">
        {loading ? (
          <Loading message="주문을 불러오는 중..." />
        ) : orders.length === 0 ? (
          <p className="no-orders">주문이 없습니다</p>
        ) : (
          <div className="orders-list">
            {orders.map((order) => (
              <div key={order.id} className="order-card">
                <div className="order-header">
                  <span className="order-number">{order.order_number}</span>
                  <span 
                    className="order-status"
                    style={{ backgroundColor: getStatusColor(order.status) }}
                  >
                    {formatOrderStatus(order.status)}
                  </span>
                </div>
                
                <div className="order-time">{formatDateTime(order.created_at)}</div>
                
                <div className="order-items">
                  {order.items.map((item) => (
                    <div key={item.id} className="order-item">
                      <span>{item.menu_name} x {item.quantity}</span>
                      <span>{formatPrice(item.subtotal)}</span>
                    </div>
                  ))}
                </div>
                
                <div className="order-total">
                  <span>합계</span>
                  <span>{formatPrice(order.total_amount)}</span>
                </div>
                
                <div className="order-actions">
                  {order.status !== 'completed' && (
                    <Button 
                      size="small"
                      variant={order.status === 'pending' ? 'warning' : 'success'}
                      onClick={() => handleStatusChange(order.id, order.status)}
                    >
                      {order.status === 'pending' ? '준비 시작' : '완료'}
                    </Button>
                  )}
                  <Button 
                    size="small" 
                    variant="danger"
                    onClick={() => handleDelete(order.id)}
                  >
                    삭제
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Modal>
  )
}
