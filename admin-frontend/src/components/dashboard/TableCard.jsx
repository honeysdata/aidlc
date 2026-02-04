import { formatPrice } from '../../utils/format'
import './TableCard.css'

export function TableCard({ table, onSelect, onComplete }) {
  const hasOrders = table.order_count > 0

  return (
    <div 
      className={`table-card ${table.is_active ? 'active' : 'inactive'}`}
      onClick={() => onSelect(table)}
    >
      <div className="table-header">
        <span className="table-number">테이블 {table.table_number}</span>
        <span className={`table-status ${table.is_active ? 'in-use' : ''}`}>
          {table.is_active ? '이용중' : '비어있음'}
        </span>
      </div>
      
      {table.is_active && (
        <>
          <div className="table-info">
            <div className="info-row">
              <span>주문 수</span>
              <span>{table.order_count}건</span>
            </div>
            <div className="info-row total">
              <span>총 금액</span>
              <span>{formatPrice(table.total_amount)}</span>
            </div>
          </div>
          
          <button 
            className="complete-btn"
            onClick={(e) => {
              e.stopPropagation()
              onComplete(table)
            }}
          >
            이용 완료
          </button>
        </>
      )}
    </div>
  )
}
