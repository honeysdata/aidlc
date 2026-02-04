// 가격 포맷팅 (원화)
export function formatPrice(price) {
  return new Intl.NumberFormat('ko-KR').format(price) + '원'
}

// 날짜/시간 포맷팅
export function formatDateTime(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

// 주문 상태 한글 변환
export function formatOrderStatus(status) {
  const statusMap = {
    PENDING: '대기중',
    PREPARING: '준비중',
    COMPLETED: '완료',
  }
  return statusMap[status] || status
}
