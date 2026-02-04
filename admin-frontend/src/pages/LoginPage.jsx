import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '../components/common/Button'
import './LoginPage.css'

export function LoginPage() {
  const [storeId, setStoreId] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { login, loading, error } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await login(storeId, username, password)
      navigate('/')
    } catch (err) {
      // error handled in context
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>테이블 오더</h1>
        <p className="login-subtitle">관리자 로그인</p>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="storeId">매장 ID</label>
            <input
              id="storeId"
              type="text"
              value={storeId}
              onChange={(e) => setStoreId(e.target.value)}
              placeholder="매장 ID"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="username">사용자명</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="사용자명"
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
              placeholder="비밀번호"
              required
            />
          </div>
          
          {error && <p className="login-error">{error}</p>}
          
          <Button type="submit" size="large" loading={loading} className="login-btn">
            로그인
          </Button>
        </form>
      </div>
    </div>
  )
}
