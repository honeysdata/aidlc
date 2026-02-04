import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const adminApi = {
  // Auth
  login: (data) => client.post('/admin/auth/login', data),
  
  // Orders
  getOrdersBySession: (sessionId) => client.get(`/admin/orders/session/${sessionId}`),
  updateOrderStatus: (orderId, status) => 
    client.patch(`/admin/orders/${orderId}/status`, { status }),
  deleteOrder: (orderId) => client.delete(`/admin/orders/${orderId}`),
  
  // Tables
  getTables: () => client.get('/admin/tables'),
  getDashboard: () => client.get('/admin/tables/dashboard'),
  createTable: (data) => client.post('/admin/tables', data),
  updateTable: (tableId, data) => client.patch(`/admin/tables/${tableId}`, data),
  deleteTable: (tableId) => client.delete(`/admin/tables/${tableId}`),
  completeTable: (tableId) => client.post(`/admin/tables/${tableId}/complete`),
  getTableHistory: (tableId, params) => 
    client.get(`/admin/tables/${tableId}/history`, { params }),
  
  // Menus
  getMenus: () => client.get('/admin/menus'),
  createMenu: (data) => client.post('/admin/menus', data),
  updateMenu: (menuId, data) => client.patch(`/admin/menus/${menuId}`, data),
  deleteMenu: (menuId) => client.delete(`/admin/menus/${menuId}`),
  
  // Categories
  getCategories: () => client.get('/admin/categories'),
  createCategory: (data) => client.post('/admin/categories', data),
  updateCategory: (categoryId, data) => 
    client.patch(`/admin/categories/${categoryId}`, data),
  deleteCategory: (categoryId) => client.delete(`/admin/categories/${categoryId}`),
}

export default client
