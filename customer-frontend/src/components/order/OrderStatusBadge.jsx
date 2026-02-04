import { formatOrderStatus } from '../../utils/format'
import './OrderStatusBadge.css'

export function OrderStatusBadge({ status }) {
  return (
    <span className={`order-status-badge status-${status.toLowerCase()}`}>
      {formatOrderStatus(status)}
    </span>
  )
}
