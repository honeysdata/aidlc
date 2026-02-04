import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, User, Table, TableSession, Category, Menu, Order, OrderItem, OrderStatus
from app.repositories.store import StoreRepository
from app.repositories.user import UserRepository
from app.repositories.table import TableRepository, TableSessionRepository
from app.repositories.category import CategoryRepository
from app.repositories.menu import MenuRepository
from app.repositories.order import OrderRepository, OrderItemRepository


@pytest.mark.asyncio
async def test_store_repository(db_session: AsyncSession):
    repo = StoreRepository()
    
    # Create
    store = await repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    assert store.id is not None
    
    # Get by store_id
    found = await repo.get_by_store_id(db_session, "test-store")
    assert found is not None
    assert found.name == "테스트 매장"
    
    # Get by id
    found_by_id = await repo.get(db_session, store.id)
    assert found_by_id is not None


@pytest.mark.asyncio
async def test_user_repository(db_session: AsyncSession):
    store_repo = StoreRepository()
    user_repo = UserRepository()
    
    store = await store_repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    
    # Create user
    user = await user_repo.create(db_session, User(
        store_id=store.id,
        username="admin",
        password_hash="hashed"
    ))
    assert user.id is not None
    
    # Get by username
    found = await user_repo.get_by_username(db_session, store.id, "admin")
    assert found is not None
    assert found.username == "admin"


@pytest.mark.asyncio
async def test_table_repository(db_session: AsyncSession):
    store_repo = StoreRepository()
    table_repo = TableRepository()
    session_repo = TableSessionRepository()
    
    store = await store_repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    
    # Create table
    table = await table_repo.create(db_session, Table(
        store_id=store.id,
        table_number=1,
        password_hash="hashed"
    ))
    assert table.id is not None
    
    # Get by table number
    found = await table_repo.get_by_table_number(db_session, store.id, 1)
    assert found is not None
    
    # Create session
    session = await session_repo.create(db_session, TableSession(table_id=table.id))
    assert session.id is not None
    assert session.is_active is True
    
    # Get active session
    active = await session_repo.get_active_session(db_session, table.id)
    assert active is not None
    assert active.id == session.id


@pytest.mark.asyncio
async def test_category_repository(db_session: AsyncSession):
    store_repo = StoreRepository()
    category_repo = CategoryRepository()
    
    store = await store_repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    
    # Create categories
    cat1 = await category_repo.create(db_session, Category(
        store_id=store.id, name="음료", display_order=1
    ))
    cat2 = await category_repo.create(db_session, Category(
        store_id=store.id, name="디저트", display_order=2
    ))
    
    # Get by store
    categories = await category_repo.get_by_store(db_session, store.id)
    assert len(categories) == 2
    assert categories[0].name == "음료"  # Ordered by display_order


@pytest.mark.asyncio
async def test_menu_repository(db_session: AsyncSession):
    store_repo = StoreRepository()
    category_repo = CategoryRepository()
    menu_repo = MenuRepository()
    
    store = await store_repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    category = await category_repo.create(db_session, Category(
        store_id=store.id, name="음료", display_order=1
    ))
    
    # Create menu
    menu = await menu_repo.create(db_session, Menu(
        store_id=store.id,
        category_id=category.id,
        name="아메리카노",
        price=4500
    ))
    assert menu.id is not None
    
    # Get by category
    menus = await menu_repo.get_by_category(db_session, category.id)
    assert len(menus) == 1
    assert menus[0].name == "아메리카노"
    
    # Get by store
    all_menus = await menu_repo.get_by_store(db_session, store.id)
    assert len(all_menus) == 1


@pytest.mark.asyncio
async def test_order_repository(db_session: AsyncSession):
    # Setup
    store_repo = StoreRepository()
    table_repo = TableRepository()
    session_repo = TableSessionRepository()
    category_repo = CategoryRepository()
    menu_repo = MenuRepository()
    order_repo = OrderRepository()
    
    store = await store_repo.create(db_session, Store(store_id="test-store", name="테스트 매장"))
    table = await table_repo.create(db_session, Table(store_id=store.id, table_number=1, password_hash="h"))
    session = await session_repo.create(db_session, TableSession(table_id=table.id))
    category = await category_repo.create(db_session, Category(store_id=store.id, name="음료", display_order=1))
    menu = await menu_repo.create(db_session, Menu(store_id=store.id, category_id=category.id, name="아메리카노", price=4500))
    
    # Create order
    order = await order_repo.create(db_session, Order(
        session_id=session.id,
        order_number="20260204-001",
        total_amount=9000
    ))
    assert order.id is not None
    
    # Get by session
    orders = await order_repo.get_by_session(db_session, session.id)
    assert len(orders) == 1
    
    # Update status
    order.status = OrderStatus.PREPARING
    updated = await order_repo.update(db_session, order)
    assert updated.status == OrderStatus.PREPARING
