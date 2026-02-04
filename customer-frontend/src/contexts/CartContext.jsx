import { createContext, useContext } from 'react'
import { useLocalStorage } from '../hooks/useLocalStorage'

const CartContext = createContext(null)

export function CartProvider({ children }) {
  const [items, setItems, clearItems] = useLocalStorage('cart', [])

  // 장바구니에 메뉴 추가
  const addItem = (menu) => {
    setItems((prev) => {
      const existing = prev.find((item) => item.id === menu.id)
      if (existing) {
        return prev.map((item) =>
          item.id === menu.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      return [...prev, { ...menu, quantity: 1 }]
    })
  }

  // 수량 증가
  const increaseQuantity = (menuId) => {
    setItems((prev) =>
      prev.map((item) =>
        item.id === menuId
          ? { ...item, quantity: item.quantity + 1 }
          : item
      )
    )
  }

  // 수량 감소 (0이 되면 삭제)
  const decreaseQuantity = (menuId) => {
    setItems((prev) =>
      prev
        .map((item) =>
          item.id === menuId
            ? { ...item, quantity: item.quantity - 1 }
            : item
        )
        .filter((item) => item.quantity > 0)
    )
  }

  // 항목 삭제
  const removeItem = (menuId) => {
    setItems((prev) => prev.filter((item) => item.id !== menuId))
  }

  // 장바구니 비우기
  const clearCart = () => {
    clearItems()
  }

  // 총 수량
  const totalQuantity = items.reduce((sum, item) => sum + item.quantity, 0)

  // 총 금액
  const totalAmount = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )

  return (
    <CartContext.Provider
      value={{
        items,
        addItem,
        increaseQuantity,
        decreaseQuantity,
        removeItem,
        clearCart,
        totalQuantity,
        totalAmount,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
