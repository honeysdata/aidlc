import { useState, useEffect } from 'react'
import { Layout } from '../components/layout/Layout'
import { CategoryTabs } from '../components/menu/CategoryTabs'
import { MenuList } from '../components/menu/MenuList'
import { Loading } from '../components/common/Loading'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { customerApi } from '../api/client'
import './MenuPage.css'

export function MenuPage() {
  const [categories, setCategories] = useState([])
  const [menus, setMenus] = useState([])
  const [activeCategory, setActiveCategory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const [categoriesRes, menusRes] = await Promise.all([
        customerApi.getCategories(),
        customerApi.getMenus(),
      ])
      
      setCategories(categoriesRes.data.categories)
      setMenus(menusRes.data.menus)
    } catch (err) {
      setError('메뉴를 불러오는데 실패했습니다')
    } finally {
      setLoading(false)
    }
  }

  const filteredMenus = activeCategory
    ? menus.filter((menu) => menu.category_id === activeCategory)
    : menus

  if (loading) {
    return (
      <Layout>
        <Loading message="메뉴를 불러오는 중..." />
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout>
        <ErrorMessage message={error} onRetry={loadData} />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="menu-page">
        <CategoryTabs
          categories={categories}
          activeId={activeCategory}
          onSelect={setActiveCategory}
        />
        <MenuList menus={filteredMenus} />
      </div>
    </Layout>
  )
}
