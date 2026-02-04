import { OrderStatusBadge } from './OrderStatusBadge'
import { formatPrice, formatDateTime } from '../../utils/format'
import './OrderItem.css'

export function OrderItem({ order }) {
  return (
    <div className="order-card">
      <div className="order-header">
        <span className="order-number">{order.order_number}</span>
        <OrderStatusBadge status={order.status} />
      </div>
      
      <div className="order-time">
        {formatDateTime(order.created_at)}
      </div>
      
      <div className="order-items-list">
        {order.items.map((item) => (
          <div key={item.id} className="order-menu-item">
            <span>{item.menu_name}</span>
            <span>x {item.quantity}</span>
          </div>
        ))}
      </div>
      
      <div className="order-total">
        <span>총 금액</span>
        <span>{formatPrice(order.total_amount)}</span>
      </div>
    </div>
  )
}
