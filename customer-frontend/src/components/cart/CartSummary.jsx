import { formatPrice } from '../../utils/format'
import './CartSummary.css'

export function CartSummary({ totalQuantity, totalAmount }) {
  return (
    <div className="cart-summary">
      <div className="cart-summary-row">
        <span>총 수량</span>
        <span>{totalQuantity}개</span>
      </div>
      <div className="cart-summary-row total">
        <span>총 금액</span>
        <span>{formatPrice(totalAmount)}</span>
      </div>
    </div>
  )
}
