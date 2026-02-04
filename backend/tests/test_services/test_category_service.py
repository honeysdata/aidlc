import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, Category, Menu
from app.services.category import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.errors import AppException


@pytest.mark.asyncio
async def test_get_categories_by_store(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    cat1 = Category(store_id=store.id, name="메인", display_order=1)
    cat2 = Category(store_id=store.id, name="사이드", display_order=2)
    db_session.add_all([cat1, cat2])
    await db_session.commit()
    
    # Test
    service = CategoryService()
    categories = await service.get_categories_by_store(db_session, store.id)
    
    assert len(categories) == 2
    assert categories[0].name == "메인"
    assert categories[1].name == "사이드"


@pytest.mark.asyncio
async def test_create_category(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    # Test
    service = CategoryService()
    data = CategoryCreate(name="새 카테고리", display_order=1)
    category = await service.create_category(db_session, store.id, data)
    
    assert category.id is not None
    assert category.name == "새 카테고리"
    assert category.store_id == store.id


@pytest.mark.asyncio
async def test_create_category_duplicate_name(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    existing = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(existing)
    await db_session.commit()
    
    # Test
    service = CategoryService()
    data = CategoryCreate(name="메인", display_order=2)
    
    with pytest.raises(AppException) as exc_info:
        await service.create_category(db_session, store.id, data)
    
    assert exc_info.value.code == "DUPLICATE"


@pytest.mark.asyncio
async def test_update_category(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="원래 이름", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    # Test
    service = CategoryService()
    data = CategoryUpdate(name="수정된 이름")
    updated = await service.update_category(db_session, store.id, category.id, data)
    
    assert updated.name == "수정된 이름"


@pytest.mark.asyncio
async def test_delete_category_success(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="삭제할 카테고리", display_order=1)
    db_session.add(category)
    await db_session.commit()
    category_id = category.id
    
    # Test
    service = CategoryService()
    await service.delete_category(db_session, store.id, category_id)
    
    # Verify deletion
    deleted = await service.category_repo.get_by_id(db_session, category_id)
    assert deleted is None


@pytest.mark.asyncio
async def test_delete_category_with_menus_fails(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메뉴있는 카테고리", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(
        store_id=store.id,
        category_id=category.id,
        name="메뉴",
        price=8000
    )
    db_session.add(menu)
    await db_session.commit()
    
    # Test
    service = CategoryService()
    with pytest.raises(AppException) as exc_info:
        await service.delete_category(db_session, store.id, category.id)
    
    assert exc_info.value.code == "CATEGORY_HAS_MENUS"
