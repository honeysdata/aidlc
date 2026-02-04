import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '../components/common/Button'
import './SetupPage.css'

export function SetupPage() {
  const [storeId, setStoreId] = useState('')
  const [tableNumber, setTableNumber] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const { login, error } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await login(storeId, parseInt(tableNumber), password)
      navigate('/menu')
    } catch (err) {
      // 에러는 AuthContext에서 처리
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="setup-page">
      <div className="setup-container">
        <h1 className="setup-title">테이블 오더</h1>
        <p className="setup-subtitle">테이블 설정</p>
        
        <form onSubmit={handleSubmit} className="setup-form">
          <div className="form-group">
            <label htmlFor="storeId">매장 ID</label>
            <input
              id="storeId"
              type="text"
              value={storeId}
              onChange={(e) => setStoreId(e.target.value)}
              placeholder="매장 ID를 입력하세요"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="tableNumber">테이블 번호</label>
            <input
              id="tableNumber"
              type="number"
              value={tableNumber}
              onChange={(e) => setTableNumber(e.target.value)}
              placeholder="테이블 번호를 입력하세요"
              min="1"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">비밀번호</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호를 입력하세요"
              minLength="4"
              required
            />
          </div>
          
          {error && <p className="setup-error">{error}</p>}
          
          <Button type="submit" size="large" loading={loading}>
            설정 완료
          </Button>
        </form>
      </div>
    </div>
  )
}
