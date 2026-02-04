import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터: 토큰 추가
client.interceptors.request.use((config) => {
  const tokenRaw = localStorage.getItem('token')
  if (tokenRaw) {
    try {
      const token = JSON.parse(tokenRaw)
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    } catch {
      // JSON 파싱 실패 시 원본 값 사용
      config.headers.Authorization = `Bearer ${tokenRaw}`
    }
  }
  return config
})

// 응답 인터셉터: 에러 처리
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('auth')
      window.location.href = '/setup'
    }
    return Promise.reject(error)
  }
)

// Customer API
export const customerApi = {
  // Auth
  login: (data) => client.post('/customer/auth/login', data),
  checkSession: () => client.get('/customer/auth/session/check'),
  
  // Menu
  getCategories: () => client.get('/customer/menu/categories'),
  getMenus: () => client.get('/customer/menu'),
  getMenusByCategory: (categoryId) => client.get(`/customer/menu/category/${categoryId}`),
  
  // Order
  createOrder: (data) => client.post('/customer/orders', data),
  getOrders: () => client.get('/customer/orders'),
}

export default client
