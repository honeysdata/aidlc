import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { CartProvider } from './contexts/CartContext'
import { SetupPage } from './pages/SetupPage'
import { MenuPage } from './pages/MenuPage'
import { CartPage } from './pages/CartPage'
import { OrderConfirmPage } from './pages/OrderConfirmPage'
import { OrderSuccessPage } from './pages/OrderSuccessPage'
import { OrderHistoryPage } from './pages/OrderHistoryPage'
import { Loading } from './components/common/Loading'
import './App.css'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return <Loading message="로그인 중..." />
  }

  if (!isAuthenticated) {
    return <Navigate to="/setup" replace />
  }

  return children
}

function AppRoutes() {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return <Loading message="로딩 중..." />
  }

  return (
    <Routes>
      <Route 
        path="/setup" 
        element={
          isAuthenticated ? <Navigate to="/menu" replace /> : <SetupPage />
        } 
      />
      <Route
        path="/menu"
        element={
          <ProtectedRoute>
            <MenuPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/cart"
        element={
          <ProtectedRoute>
            <CartPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/order/confirm"
        element={
          <ProtectedRoute>
            <OrderConfirmPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/order/success"
        element={
          <ProtectedRoute>
            <OrderSuccessPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/orders"
        element={
          <ProtectedRoute>
            <OrderHistoryPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/menu" replace />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <AppRoutes />
      </CartProvider>
    </AuthProvider>
  )
}

export default App
