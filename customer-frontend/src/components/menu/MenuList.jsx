import { MenuCard } from './MenuCard'
import './MenuList.css'

export function MenuList({ menus }) {
  if (menus.length === 0) {
    return (
      <div className="menu-empty">
        <p>메뉴가 없습니다</p>
      </div>
    )
  }

  return (
    <div className="menu-list">
      {menus.map((menu) => (
        <MenuCard key={menu.id} menu={menu} />
      ))}
    </div>
  )
}
