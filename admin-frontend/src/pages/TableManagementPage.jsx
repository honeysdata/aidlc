import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import { Button } from '../components/common/Button'
import { Modal, ConfirmDialog } from '../components/common/Modal'
import { Loading } from '../components/common/Loading'
import { adminApi } from '../api/client'
import './TableManagementPage.css'

export function TableManagementPage() {
  const [tables, setTables] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editTarget, setEditTarget] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [formData, setFormData] = useState({ table_number: '', password: '' })
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const navigate = useNavigate()

  const loadTables = async () => {
    try {
      const response = await adminApi.getTables()
      setTables(response.data.tables)
    } catch (err) {
      console.error('Failed to load tables:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTables()
  }, [])

  const handleAdd = () => {
    setEditTarget(null)
    setFormData({ table_number: '', password: '' })
    setShowForm(true)
  }

  const handleEdit = (table) => {
    setEditTarget(table)
    setFormData({ table_number: table.table_number, password: '' })
    setShowForm(true)
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    
    try {
      if (editTarget) {
        if (formData.password) {
          await adminApi.updateTable(editTarget.id, { password: formData.password })
        }
      } else {
        await adminApi.createTable({
          table_number: parseInt(formData.table_number),
          password: formData.password,
        })
      }
      setShowForm(false)
      loadTables()
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
      await adminApi.deleteTable(deleteTarget.id)
      setDeleteTarget(null)
      loadTables()
    } catch (err) {
      alert(err.response?.data?.error?.message || '삭제에 실패했습니다')
    } finally {
      setDeleting(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <Loading message="테이블 목록을 불러오는 중..." />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="table-management-page">
        <div className="page-header">
          <h1>테이블 관리</h1>
          <Button onClick={handleAdd}>+ 테이블 추가</Button>
        </div>
        
        <div className="table-list">
          <table>
            <thead>
              <tr>
                <th>테이블 번호</th>
                <th>작업</th>
              </tr>
            </thead>
            <tbody>
              {tables.map((table) => (
                <tr key={table.id}>
                  <td>테이블 {table.table_number}</td>
                  <td className="actions">
                    <Button size="small" variant="ghost" onClick={() => navigate(`/tables/${table.id}/history`)}>
                      과거 내역
                    </Button>
                    <Button size="small" variant="secondary" onClick={() => handleEdit(table)}>
                      비밀번호 변경
                    </Button>
                    <Button size="small" variant="danger" onClick={() => setDeleteTarget(table)}>
                      삭제
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {tables.length === 0 && (
            <div className="empty-state">
              <p>등록된 테이블이 없습니다</p>
            </div>
          )}
        </div>
      </div>
      
      <Modal
        isOpen={showForm}
        onClose={() => setShowForm(false)}
        title={editTarget ? '비밀번호 변경' : '테이블 추가'}
      >
        <form onSubmit={handleSave} className="table-form">
          {!editTarget && (
            <div className="form-group">
              <label>테이블 번호</label>
              <input
                type="number"
                value={formData.table_number}
                onChange={(e) => setFormData({ ...formData, table_number: e.target.value })}
                min="1"
                required
              />
            </div>
          )}
          
          <div className="form-group">
            <label>비밀번호 {editTarget && '(변경 시에만 입력)'}</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              minLength="4"
              required={!editTarget}
              placeholder={editTarget ? '새 비밀번호' : '비밀번호'}
            />
          </div>
          
          <div className="form-actions">
            <Button type="button" variant="secondary" onClick={() => setShowForm(false)}>
              취소
            </Button>
            <Button type="submit" loading={saving}>
              {editTarget ? '변경' : '추가'}
            </Button>
          </div>
        </form>
      </Modal>
      
      <ConfirmDialog
        isOpen={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        title="테이블 삭제"
        message={`테이블 ${deleteTarget?.table_number}을(를) 삭제하시겠습니까?`}
        confirmText="삭제"
        loading={deleting}
      />
    </Layout>
  )
}
