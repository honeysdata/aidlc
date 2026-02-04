import { createContext, useContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { customerApi } from '../api/client'
import { useLocalStorage } from '../hooks/useLocalStorage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [auth, setAuth, removeAuth] = useLocalStorage('auth', null)
  const [token, setToken, removeToken] = useLocalStorage('token', null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  // 앱 시작 시 자동 로그인 시도
  useEffect(() => {
    const autoLogin = async () => {
      if (auth && !token) {
        try {
          await login(auth.storeId, auth.tableNumber, auth.password)
        } catch (err) {
          console.error('Auto login failed:', err)
          removeAuth()
          removeToken()
        }
      }
      setLoading(false)
    }
    autoLogin()
  }, [])

  const login = async (storeId, tableNumber, password) => {
    setError(null)
    try {
      const response = await customerApi.login({
        store_id: storeId,
        table_number: tableNumber,
        password: password,
      })
      
      const { token: newToken, session_id } = response.data
      
      setToken(newToken)
      setAuth({
        storeId,
        tableNumber,
        password,
        sessionId: session_id,
      })
      
      return response.data
    } catch (err) {
      const message = err.response?.data?.error?.message || '로그인에 실패했습니다'
      setError(message)
      throw err
    }
  }

  const logout = () => {
    removeToken()
    removeAuth()
    navigate('/setup')
  }

  const isAuthenticated = !!token

  return (
    <AuthContext.Provider
      value={{
        auth,
        token,
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
