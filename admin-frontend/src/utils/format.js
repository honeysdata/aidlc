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
    pending: '대기중',
    preparing: '준비중',
    completed: '완료',
  }
  return statusMap[status] || status
}

export function getStatusColor(status) {
  const colorMap = {
    pending: '#f39c12',
    preparing: '#3498db',
    completed: '#27ae60',
  }
  return colorMap[status] || '#666'
}
