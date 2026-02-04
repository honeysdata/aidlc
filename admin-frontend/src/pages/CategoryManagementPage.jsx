import { useState, useEffect } from 'react'
import { Layout } from '../components/layout/Layout'
import { Button } from '../components/common/Button'
import { Modal, ConfirmDialog } from '../components/common/Modal'
import { Loading } from '../components/common/Loading'
import { adminApi } from '../api/client'
import './CategoryManagementPage.css'

export function CategoryManagementPage() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editTarget, setEditTarget] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [formData, setFormData] = useState({ name: '', display_order: 0 })
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const loadCategories = async () => {
    try {
      const response = await adminApi.getCategories()
      setCategories(response.data.categories)
    } catch (err) {
      console.error('Failed to load categories:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCategories()
  }, [])

  const handleAdd = () => {
    setEditTarget(null)
    setFormData({ name: '', display_order: 0 })
    setShowForm(true)
  }

  const handleEdit = (category) => {
    setEditTarget(category)
    setFormData({ name: category.name, display_order: category.display_order })
    setShowForm(true)
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    try {
      if (editTarget) {
        await adminApi.updateCategory(editTarget.id, formData)
      } else {
        await adminApi.createCategory(formData)
      }
      setShowForm(false)
      loadCategories()
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
      await adminApi.deleteCategory(deleteTarget.id)
      setDeleteTarget(null)
      loadCategories()
    } catch (err) {
      alert(err.response?.data?.error?.message || '삭제에 실패했습니다')
    } finally {
      setDeleting(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <Loading message="카테고리 목록을 불러오는 중..." />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="category-management-page">
        <div className="page-header">
          <h1>카테고리 관리</h1>
          <Button onClick={handleAdd}>+ 카테고리 추가</Button>
        </div>
        
        <div className="category-list">
          <table>
            <thead>
              <tr>
                <th>카테고리명</th>
                <th>표시 순서</th>
                <th>작업</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((category) => (
                <tr key={category.id}>
                  <td>{category.name}</td>
                  <td>{category.display_order}</td>
                  <td className="actions">
                    <Button size="small" variant="secondary" onClick={() => handleEdit(category)}>
                      수정
                    </Button>
                    <Button size="small" variant="danger" onClick={() => setDeleteTarget(category)}>
                      삭제
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {categories.length === 0 && (
            <div className="empty-state">
              <p>등록된 카테고리가 없습니다</p>
            </div>
          )}
        </div>
      </div>
      
      <Modal
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        title={editTarget ? '카테고리 수정' : '카테고리 추가'}
      >
        <form onSubmit={handleSave} className="category-form">
          <div className="form-group">
            <label>카테고리명 *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          
          <div className="form-group">
            <label>표시 순서</label>
            <input
              type="number"
              value={formData.display_order}
              onChange={(e) => setFormData({ ...formData, display_order: parseInt(e.target.value) })}
            />
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
        title="카테고리 삭제"
        message={`"${deleteTarget?.name}" 카테고리를 삭제하시겠습니까? 메뉴가 있는 카테고리는 삭제할 수 없습니다.`}
        confirmText="삭제"
        loading={deleting}
      />
    </Layout>
  )
}
