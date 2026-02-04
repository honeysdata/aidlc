import { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import './OrderSuccessPage.css'

export function OrderSuccessPage() {
  const [countdown, setCountdown] = useState(5)
  const navigate = useNavigate()
  const location = useLocation()
  const orderNumber = location.state?.orderNumber

  useEffect(() => {
    if (!orderNumber) {
      navigate('/menu')
      return
    }

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          navigate('/menu')
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [navigate, orderNumber])

  if (!orderNumber) {
    return null
  }

  return (
    <div className="order-success-page">
      <div className="success-container">
        <div className="success-icon">✓</div>
        <h1>주문 완료!</h1>
        <p className="order-number">주문번호: {orderNumber}</p>
        <p className="success-message">
          주문이 접수되었습니다.<br />
          잠시만 기다려주세요.
        </p>
        <p className="redirect-message">
          {countdown}초 후 메뉴 화면으로 이동합니다
        </p>
        <button 
          className="go-menu-btn"
          onClick={() => navigate('/menu')}
        >
          메뉴로 바로가기
        </button>
      </div>
    </div>
  )
}
