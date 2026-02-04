import { useState, useEffect } from 'react'
import { Layout } from '../components/layout/Layout'
import { Button } from '../components/common/Button'
import { Modal, ConfirmDialog } from '../components/common/Modal'
import { Loading } from '../components/common/Loading'
import { adminApi } from '../api/client'
import { formatPrice } from '../utils/format'
import './MenuManagementPage.css'

export function MenuManagementPage() {
  const [menus, setMenus] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editTarget, setEditTarget] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    description: '',
    category_id: '',
    display_order: 0,
    is_available: true,
  })
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const loadData = async () => {
    try {
      const [menusRes, categoriesRes] = await Promise.all([
        adminApi.getMenus(),
        adminApi.getCategories(),
      ])
      setMenus(menusRes.data.menus)
      setCategories(categoriesRes.data.categories)
    } catch (err) {
      console.error('Failed to load data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const handleAdd = () => {
    setEditTarget(null)
    setFormData({
      name: '',
      price: '',
      description: '',
      category_id: categories[0]?.id || '',
      display_order: 0,
      is_available: true,
    })
    setShowForm(true)
  }

  const handleEdit = (menu) => {
    setEditTarget(menu)
    setFormData({
      name: menu.name,
      price: menu.price,
      description: menu.description || '',
      category_id: menu.category_id,
      display_order: menu.display_order,
      is_available: menu.is_available,
    })
    setShowForm(true)
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    try {
      const data = {
        ...formData,
        price: parseInt(formData.price),
        category_id: parseInt(formData.category_id),
      }
      
      if (editTarget) {
        await adminApi.updateMenu(editTarget.id, data)
      } else {
        await adminApi.createMenu(data)
      }
      setShowForm(false)
      loadData()
    } catch (err) {
      alert(err.response?.data?.error?.message || '저장에 실패했습니다')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    
    setDeleting(true)
    try {
      await adminApi.deleteMenu(deleteTarget.id)
      setDeleteTarget(null)
      loadData()
    } catch (err) {
      alert(err.response?.data?.error?.message || '삭제에 실패했습니다')
    } finally {
      setDeleting(false)
    }
  }

  const getCategoryName = (categoryId) => {
    return categories.find(c => c.id === categoryId)?.name || '-'
  }

  if (loading) {
    return (
      <Layout>
        <Loading message="메뉴 목록을 불러오는 중..." />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="menu-management-page">
        <div className="page-header">
          <h1>메뉴 관리</h1>
          <Button onClick={handleAdd}>+ 메뉴 추가</Button>
        </div>
        
        <div className="menu-list">
          <table>
            <thead>
              <tr>
                <th>메뉴명</th>
                <th>가격</th>
                <th>카테고리</th>
                <th>상태</th>
                <th>작업</th>
              </tr>
            </thead>
            <tbody>
              {menus.map((menu) => (
                <tr key={menu.id} className={!menu.is_available ? 'unavailable' : ''}>
                  <td>{menu.name}</td>
                  <td>{formatPrice(menu.price)}</td>
                  <td>{getCategoryName(menu.category_id)}</td>
                  <td>
                    <span className={`status-badge ${menu.is_available ? 'available' : 'sold-out'}`}>
                      {menu.is_available ? '판매중' : '품절'}
                    </span>
                  </td>
                  <td className="actions">
                    <Button size="small" variant="secondary" onClick={() => handleEdit(menu)}>
                      수정
                    </Button>
                    <Button size="small" variant="danger" onClick={() => setDeleteTarget(menu)}>
                      삭제
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {menus.length === 0 && (
            <div className="empty-state">
              <p>등록된 메뉴가 없습니다</p>
            </div>
          )}
        </div>
      </div>
      
      <Modal
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        title={editTarget ? '메뉴 수정' : '메뉴 추가'}
      >
        <form onSubmit={handleSave} className="menu-form">
          <div className="form-group">
            <label>메뉴명 *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>가격 *</label>
            <input
              type="number"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              min="0"
              required
            />
          </div>
          
          <div className="form-group">
            <label>설명</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows="3"
            />
          </div>
          
          <div className="form-group">
            <label>카테고리 *</label>
            <select
              value={formData.category_id}
              onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
              required
            >
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label>표시 순서</label>
            <input
              type="number"
              value={formData.display_order}
              onChange={(e) => setFormData({ ...formData, display_order: parseInt(e.target.value) })}
            />
          </div>
          
          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                checked={formData.is_available}
                onChange={(e) => setFormData({ ...formData, is_available: e.target.checked })}
              />
              판매중
            </label>
          </div>
          
          <div className="form-actions">
            <Button type="button" variant="secondary" onClick={() => setShowForm(false)}>
              취소
            </Button>
            <Button type="submit" loading={saving}>
              {editTarget ? '수정' : '추가'}
            </Button>
          </div>
        </form>
      </Modal>
      
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        title="메뉴 삭제"
        message={`"${deleteTarget?.name}" 메뉴를 삭제하시겠습니까?`}
        confirmText="삭제"
        loading={deleting}
      />
    </Layout>
  )
}
