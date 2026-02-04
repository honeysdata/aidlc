export function formatPrice(price) {
  return new Intl.NumberFormat('ko-KR').format(price) + '원'
}

export function formatDateTime(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

export function formatDate(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date)
}

export function formatOrderStatus(status) {
  const statusMap = {
    PENDING: '대기중',
    PREPARING: '준비중',
    COMPLETED: '완료',
  }
  return statusMap[status] || status
}

export function getStatusColor(status) {
  const colorMap = {
    PENDING: '#f39c12',
    PREPARING: '#3498db',
    COMPLETED: '#27ae60',
  }
  return colorMap[status] || '#666'
}
