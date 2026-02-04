import { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { customerApi } from '../api/client'
import { useLocalStorage } from '../hooks/useLocalStorage'
import { useSSE } from '../hooks/useSSE'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [auth, setAuth, removeAuth] = useLocalStorage('auth', null)
  const [token, setToken, removeToken] = useLocalStorage('token', null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const sessionCheckIntervalRef = useRef(null)

  const logout = useCallback(() => {
    removeToken()
    removeAuth()
    // 장바구니도 초기화
    localStorage.removeItem('cart')
    navigate('/setup')
  }, [removeToken, removeAuth, navigate])

  // 세션 유효성 확인
  const checkSession = useCallback(async () => {
    if (!token) return
    
    try {
      const response = await customerApi.checkSession()
      if (!response.data.valid) {
        alert('이용이 완료되었습니다. 감사합니다!')
        logout()
      }
    } catch (err) {
      // 401 에러는 인터셉터에서 처리됨
      if (err.response?.status !== 401) {
        console.error('Session check failed:', err)
      }
    }
  }, [token, logout])

  // SSE 이벤트 핸들러
  const handleSSEEvent = useCallback((event) => {
    if (event.type === 'session_completed') {
      // 관리자가 이용 완료 처리 시 로그아웃
      alert('이용이 완료되었습니다. 감사합니다!')
      logout()
    }
  }, [logout])

  // SSE 연결 (인증된 경우에만)
  useSSE(token ? handleSSEEvent : () => {})

  // 주기적 세션 체크 (10초마다)
  useEffect(() => {
    if (token) {
      // 초기 체크
      checkSession()
      
      // 주기적 체크
      sessionCheckIntervalRef.current = setInterval(checkSession, 10000)
      
      // 페이지 포커스 시 체크
      const handleFocus = () => checkSession()
      window.addEventListener('focus', handleFocus)
      
      return () => {
        if (sessionCheckIntervalRef.current) {
          clearInterval(sessionCheckIntervalRef.current)
        }
        window.removeEventListener('focus', handleFocus)
      }
    }
  }, [token, checkSession])

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
