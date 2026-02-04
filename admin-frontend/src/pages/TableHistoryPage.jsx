import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { Button } from '../components/common/Button'
import { Loading } from '../components/common/Loading'
import { adminApi } from '../api/client'
import { formatPrice, formatDateTime } from '../utils/format'
import './TableHistoryPage.css'

export function TableHistoryPage() {
  const { tableId } = useParams()
  const navigate = useNavigate()
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')

  const loadHistory = async () => {
    setLoading(true)
    try {
      const params = {}
      if (dateFrom) params.date_from = dateFrom
      if (dateTo) params.date_to = dateTo
      
      const response = await adminApi.getTableHistory(tableId, params)
      setHistory(response.data.orders)
    } catch (err) {
      console.error('Failed to load history:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [tableId])

  const handleFilter = (e) => {
    e.preventDefault()
    loadHistory()
  }

  return (
    <Layout>
      <div className="table-history-page">
        <div className="page-header">
          <div>
            <Button variant="ghost" onClick={() => navigate('/tables')}>
              ← 테이블 관리
            </Button>
            <h1>과거 주문 내역</h1>
          </div>
        </div>
        
        <form className="filter-form" onSubmit={handleFilter}>
          <div className="filter-group">
            <label>시작일</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
            />
          </div>
          <div className="filter-group">
            <label>종료일</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
            />
          </div>
          <Button type="submit">조회</Button>
        </form>
        
        {loading ? (
          <Loading message="내역을 불러오는 중..." />
        ) : (
          <div className="history-list">
            {history.length === 0 ? (
              <div className="empty-state">
                <p>과거 주문 내역이 없습니다</p>
              </div>
            ) : (
              history.map((order) => (
                <div key={order.id} className="history-card">
                  <div className="history-header">
                    <span className="order-number">{order.order_number}</span>
                    <span className="order-date">{formatDateTime(order.completed_at)}</span>
                  </div>
                  <div className="history-items">
                    {JSON.parse(order.items_json).map((item, idx) => (
                      <div key={idx} className="history-item">
                        <span>{item.menu_name} x {item.quantity}</span>
                        <span>{formatPrice(item.subtotal)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="history-total">
                    <span>합계</span>
                    <span>{formatPrice(order.total_amount)}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </Layout>
  )
}
