import { useState, useEffect, useCallback } from 'react'
import { Layout } from '../components/layout/Layout'
import { TableCard } from '../components/dashboard/TableCard'
import { OrderDetailModal } from '../components/dashboard/OrderDetailModal'
import { ConfirmDialog } from '../components/common/Modal'
import { Loading } from '../components/common/Loading'
import { adminApi } from '../api/client'
import { useSSE } from '../hooks/useSSE'
import './DashboardPage.css'

export function DashboardPage() {
  const [tables, setTables] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTable, setSelectedTable] = useState(null)
  const [completeTarget, setCompleteTarget] = useState(null)
  const [completing, setCompleting] = useState(false)
  const [newOrderIds, setNewOrderIds] = useState(new Set())

  const loadDashboard = async () => {
    try {
      const response = await adminApi.getDashboard()
      setTables(response.data.tables.map(t => ({ ...t, orders: [] })))
    } catch (err) {
      console.error('Failed to load dashboard:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  // SSE 이벤트 핸들러
  const handleSSEEvent = useCallback((event) => {
    if (event.type === 'new_order') {
      const order = event.data
      setNewOrderIds(prev => new Set([...prev, order.order_id]))
      
      // 3초 후 하이라이트 제거
      setTimeout(() => {
        setNewOrderIds(prev => {
          const next = new Set(prev)
          next.delete(order.order_id)
          return next
        })
      }, 3000)
      
      // 대시보드 새로고침
      loadDashboard()
    } else if (event.type === 'order_updated' || event.type === 'order_deleted') {
      loadDashboard()
    }
  }, [])

  useSSE(handleSSEEvent)

  const handleSelectTable = (table) => {
    if (table.is_active) {
      setSelectedTable(table)
    }
  }

  const handleComplete = async () => {
    if (!completeTarget) return
    
    setCompleting(true)
    try {
      await adminApi.completeTable(completeTarget.id)
      setCompleteTarget(null)
      loadDashboard()
    } catch (err) {
      alert(err.response?.data?.error?.message || '이용 완료 처리에 실패했습니다')
    } finally {
      setCompleting(false)
    }
  }

  const handleOrderUpdate = (orderId, newStatus) => {
    loadDashboard()
  }

  const handleOrderDelete = (orderId) => {
    loadDashboard()
    setSelectedTable(null)
  }

  if (loading) {
    return (
      <Layout>
        <Loading message="대시보드를 불러오는 중..." />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="dashboard-page">
        <div className="page-header">
          <h1>실시간 주문 현황</h1>
          <button className="refresh-btn" onClick={loadDashboard}>
            🔄 새로고침
          </button>
        </div>
        
        <div className="tables-grid">
          {tables.map((table) => (
            <TableCard
              key={table.id}
              table={table}
              onSelect={handleSelectTable}
              onComplete={(t) => setCompleteTarget(t)}
            />
          ))}
        </div>
        
        {tables.length === 0 && (
          <div className="empty-state">
            <p>등록된 테이블이 없습니다</p>
            <p>테이블 관리에서 테이블을 추가해주세요</p>
          </div>
        )}
      </div>
      
      <OrderDetailModal
        isOpen={!!selectedTable}
        onClose={() => setSelectedTable(null)}
        table={selectedTable}
        onOrderUpdate={handleOrderUpdate}
        onOrderDelete={handleOrderDelete}
      />
      
      <ConfirmDialog
        isOpen={!!completeTarget}
        onClose={() => setCompleteTarget(null)}
        onConfirm={handleComplete}
        title="이용 완료"
        message={`테이블 ${completeTarget?.table_number}의 이용을 완료하시겠습니까? 모든 주문이 과거 내역으로 이동됩니다.`}
        confirmText="이용 완료"
        loading={completing}
      />
    </Layout>
  )
}
