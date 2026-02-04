import './CategoryTabs.css'

export function CategoryTabs({ categories, activeId, onSelect }) {
  return (
    <div className="category-tabs">
      <button
        className={`category-tab ${activeId === null ? 'active' : ''}`}
        onClick={() => onSelect(null)}
      >
        전체
      </button>
      {categories.map((category) => (
        <button
          key={category.id}
          className={`category-tab ${activeId === category.id ? 'active' : ''}`}
          onClick={() => onSelect(category.id)}
        >
          {category.name}
        </button>
      ))}
    </div>
  )
}
