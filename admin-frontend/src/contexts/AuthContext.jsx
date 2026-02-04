import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { adminApi } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('admin_token'))
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('admin_user')
    return saved ? JSON.parse(saved) : null
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const login = async (storeId, username, password) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await adminApi.login({
        store_id: storeId,
        username,
        password,
      })
      
      const { token: newToken, store_id, username: userName, expires_at } = response.data
      
      localStorage.setItem('admin_token', newToken)
      localStorage.setItem('admin_user', JSON.stringify({ storeId: store_id, username: userName, expiresAt: expires_at }))
      
      setToken(newToken)
      setUser({ storeId: store_id, username: userName, expiresAt: expires_at })
      
      return response.data
    } catch (err) {
      const message = err.response?.data?.error?.message || '로그인에 실패했습니다'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    setToken(null)
    setUser(null)
    navigate('/login')
  }

  // 토큰 만료 체크
  useEffect(() => {
    if (user?.expiresAt) {
      const expiresAt = new Date(user.expiresAt)
      const now = new Date()
      
      if (now >= expiresAt) {
        logout()
      }
    }
  }, [user])

  const isAuthenticated = !!token

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        loading,
        error,
        isAuthenticated,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
