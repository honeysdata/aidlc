import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Store, User, Table, TableSession, 
    Category, Menu, Order, OrderItem, OrderStatus
)


@pytest.mark.asyncio
async def test_create_store(db_session: AsyncSession):
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    await db_session.refresh(store)
    
    assert store.id is not None
    assert store.store_id == "test-store"
    assert store.name == "테스트 매장"


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    user = User(store_id=store.id, username="admin", password_hash="hashed")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "admin"


@pytest.mark.asyncio
async def test_create_table_and_session(db_session: AsyncSession):
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hashed")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id)
    db_session.add(session)
    await db_session.commit()
    await db_session.refresh(session)
    
    assert session.id is not None
    assert session.is_active is True


@pytest.mark.asyncio
async def test_create_category_and_menu(db_session: AsyncSession):
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="음료", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(
        store_id=store.id,
        category_id=category.id,
        name="아메리카노",
        price=4500,
        description="시원한 아메리카노"
    )
    db_session.add(menu)
    await db_session.commit()
    await db_session.refresh(menu)
    
    assert menu.id is not None
    assert menu.price == 4500


@pytest.mark.asyncio
async def test_create_order_with_items(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hashed")
    db_session.add(table)
    await db_session.commit()
    
    session = TableSession(table_id=table.id)
    db_session.add(session)
    await db_session.commit()
    
    category = Category(store_id=store.id, name="음료", display_order=1)
    db_session.add(category)
    await db_session.commit()
    
    menu = Menu(store_id=store.id, category_id=category.id, name="아메리카노", price=4500)
    db_session.add(menu)
    await db_session.commit()
    
    # Create order
    order = Order(
        session_id=session.id,
        order_number="20260204-001",
        total_amount=9000
    )
    db_session.add(order)
    await db_session.commit()
    
    # Create order item with snapshot
    item = OrderItem(
        order_id=order.id,
        menu_id=menu.id,
        menu_name="아메리카노",
        unit_price=4500,
        quantity=2,
        subtotal=9000
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(order)
    
    assert order.id is not None
    assert order.status == OrderStatus.PENDING
    assert item.menu_name == "아메리카노"


@pytest.mark.asyncio
async def test_order_status_values():
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.PREPARING.value == "preparing"
    assert OrderStatus.COMPLETED.value == "completed"
