import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, Category, Menu
from app.services.menu import MenuService
from app.schemas.menu import MenuCreate, MenuUpdate
from app.utils.errors import AppException


@pytest.mark.asyncio
async def test_get_menus_by_store(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu1 = Menu(
        store_id=store.id,
        category_id=category.id,
        name="김치찌개",
        price=8000,
        display_order=1,
        is_available=True
    )
    menu2 = Menu(
        store_id=store.id,
        category_id=category.id,
        name="된장찌개",
        price=7000,
        display_order=2,
        is_available=True
    )
    menu3 = Menu(
        store_id=store.id,
        category_id=category.id,
        name="품절메뉴",
        price=9000,
        display_order=3,
        is_available=False
    )
    db_session.add_all([menu1, menu2, menu3])
    await db_session.commit()
    
    # Test
    service = MenuService()
    menus = await service.get_menus_by_store(db_session, store.id)
    
    assert len(menus) == 2  # 품절 메뉴 제외
    assert menus[0].name == "김치찌개"
    assert menus[1].name == "된장찌개"


@pytest.mark.asyncio
async def test_get_all_menus_by_store_admin(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu1 = Menu(
        store_id=store.id,
        category_id=category.id,
        name="김치찌개",
        price=8000,
        is_available=True
    )
    menu2 = Menu(
        store_id=store.id,
        category_id=category.id,
        name="품절메뉴",
        price=9000,
        is_available=False
    )
    db_session.add_all([menu1, menu2])
    await db_session.commit()
    
    # Test
    service = MenuService()
    menus = await service.get_all_menus_by_store(db_session, store.id)
    
    assert len(menus) == 2  # 품절 메뉴 포함


@pytest.mark.asyncio
async def test_create_menu(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    # Test
    service = MenuService()
    menu_data = MenuCreate(
        name="새 메뉴",
        price=10000,
        description="맛있는 메뉴",
        category_id=category.id,
        display_order=1
    )
    menu = await service.create_menu(db_session, store.id, menu_data)
    
    assert menu.id is not None
    assert menu.name == "새 메뉴"
    assert menu.price == 10000
    assert menu.store_id == store.id


@pytest.mark.asyncio
async def test_create_menu_invalid_category(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    # Test
    service = MenuService()
    menu_data = MenuCreate(
        name="새 메뉴",
        price=10000,
        category_id=9999,  # 존재하지 않는 카테고리
        display_order=1
    )
    
    with pytest.raises(AppException) as exc_info:
        await service.create_menu(db_session, store.id, menu_data)
    
    assert exc_info.value.code == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_menu(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(
        store_id=store.id,
        category_id=category.id,
        name="원래 메뉴",
        price=8000
    )
    db_session.add(menu)
    await db_session.commit()
    
    # Test
    service = MenuService()
    update_data = MenuUpdate(name="수정된 메뉴", price=9000)
    updated = await service.update_menu(db_session, store.id, menu.id, update_data)
    
    assert updated.name == "수정된 메뉴"
    assert updated.price == 9000


@pytest.mark.asyncio
async def test_delete_menu(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(
        store_id=store.id,
        category_id=category.id,
        name="삭제할 메뉴",
        price=8000
    )
    db_session.add(menu)
    await db_session.commit()
    menu_id = menu.id
    
    # Test
    service = MenuService()
    await service.delete_menu(db_session, store.id, menu_id)
    
    # Verify deletion
    deleted_menu = await service.menu_repo.get_by_id(db_session, menu_id)
    assert deleted_menu is None
