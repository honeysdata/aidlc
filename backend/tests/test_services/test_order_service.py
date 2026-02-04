import pytest
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, Table, TableSession, Category, Menu, Order, OrderItem
from app.models.order import OrderStatus
from app.services.order import OrderService
from app.schemas.order import OrderCreate, OrderItemCreate, OrderStatusUpdate
from app.utils.errors import AppException


@pytest.mark.asyncio
async def test_create_order_success(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="메인", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(
        store_id=store.id,
        category_id=category.id,
        name="김치찌개",
        price=8000,
        is_available=True
    )
    db_session.add(menu)
    await db_session.commit()
    
    # Test
    service = OrderService()
    order_data = OrderCreate(
        items=[OrderItemCreate(menu_id=menu.id, quantity=2)]
    )
    order = await service.create_order(db_session, store.id, session.id, order_data)
    
    assert order.id is not None
    assert order.order_number.startswith(date.today().strftime("%Y%m%d"))
    assert order.status == OrderStatus.PENDING
    assert order.total_amount == 16000
    assert len(order.items) == 1
    assert order.items[0].menu_name == "김치찌개"
    assert order.items[0].unit_price == 8000
    assert order.items[0].quantity == 2


@pytest.mark.asyncio
async def test_create_order_invalid_session(db_session: AsyncSession):
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
        name="김치찌개",
        price=8000
    )
    db_session.add(menu)
    await db_session.commit()
    
    # Test
    service = OrderService()
    order_data = OrderCreate(
        items=[OrderItemCreate(menu_id=menu.id, quantity=1)]
    )
    
    with pytest.raises(AppException) as exc_info:
        await service.create_order(db_session, store.id, 9999, order_data)
    
    assert exc_info.value.code == "SESSION_INVALID"


@pytest.mark.asyncio
async def test_create_order_menu_not_found(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    # Test
    service = OrderService()
    order_data = OrderCreate(
        items=[OrderItemCreate(menu_id=9999, quantity=1)]
    )
    
    with pytest.raises(AppException) as exc_info:
        await service.create_order(db_session, store.id, session.id, order_data)
    
    assert exc_info.value.code == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_order_status_valid_transition(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    order = Order(
        session_id=session.id,
        order_number="20260204-001",
        status=OrderStatus.PENDING,
        total_amount=8000
    )
    db_session.add(order)
    await db_session.commit()
    
    # Test: PENDING -> PREPARING
    service = OrderService()
    updated = await service.update_order_status(
        db_session, store.id, order.id, OrderStatusUpdate(status=OrderStatus.PREPARING)
    )
    
    assert updated.status == OrderStatus.PREPARING


@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    order = Order(
        session_id=session.id,
        order_number="20260204-001",
        status=OrderStatus.COMPLETED,
        total_amount=8000
    )
    db_session.add(order)
    await db_session.commit()
    
    # Test: COMPLETED -> PENDING (invalid)
    service = OrderService()
    with pytest.raises(AppException) as exc_info:
        await service.update_order_status(
            db_session, store.id, order.id, OrderStatusUpdate(status=OrderStatus.PENDING)
        )
    
    assert exc_info.value.code == "INVALID_STATUS_TRANSITION"


@pytest.mark.asyncio
async def test_get_orders_by_session(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    order1 = Order(
        session_id=session.id,
        order_number="20260204-001",
        status=OrderStatus.PENDING,
        total_amount=8000
    )
    order2 = Order(
        session_id=session.id,
        order_number="20260204-002",
        status=OrderStatus.COMPLETED,
        total_amount=15000
    )
    db_session.add_all([order1, order2])
    await db_session.commit()
    
    # Test
    service = OrderService()
    orders = await service.get_orders_by_session(db_session, session.id)
    
    assert len(orders) == 2


@pytest.mark.asyncio
async def test_delete_order(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session)
    await db_session.commit()
    
    order = Order(
        session_id=session.id,
        order_number="20260204-001",
        status=OrderStatus.PENDING,
        total_amount=8000
    )
    db_session.add(order)
    await db_session.commit()
    order_id = order.id
    
    # Test
    service = OrderService()
    await service.delete_order(db_session, store.id, order_id)
    
    # Verify deletion
    deleted = await service.order_repo.get_by_id(db_session, order_id)
    assert deleted is None
