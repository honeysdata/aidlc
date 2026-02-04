import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, Table, TableSession, Order
from app.models.order import OrderStatus
from app.services.table import TableService
from app.schemas.table import TableCreate, TableUpdate
from app.utils.errors import AppException
from app.utils.password import password_hasher


@pytest.mark.asyncio
async def test_get_tables_by_store(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table1 = Table(store_id=store.id, table_number=1, password_hash="hash1")
    table2 = Table(store_id=store.id, table_number=2, password_hash="hash2")
    db_session.add_all([table1, table2])
    await db_session.commit()
    
    # Test
    service = TableService()
    tables = await service.get_tables_by_store(db_session, store.id)
    
    assert len(tables) == 2
    assert tables[0].table_number == 1
    assert tables[1].table_number == 2


@pytest.mark.asyncio
async def test_create_table(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    # Test
    service = TableService()
    data = TableCreate(table_number=1, password="1234")
    table = await service.create_table(db_session, store.id, data)
    
    assert table.id is not None
    assert table.table_number == 1
    assert password_hasher.verify("1234", table.password_hash)


@pytest.mark.asyncio
async def test_create_table_duplicate_number(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    existing = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(existing)
    await db_session.commit()
    
    # Test
    service = TableService()
    data = TableCreate(table_number=1, password="1234")
    
    with pytest.raises(AppException) as exc_info:
        await service.create_table(db_session, store.id, data)
    
    assert exc_info.value.code == "DUPLICATE"


@pytest.mark.asyncio
async def test_update_table_password(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(
        store_id=store.id,
        table_number=1,
        password_hash=password_hasher.hash("old_pass")
    )
    db_session.add(table)
    await db_session.commit()
    
    # Test
    service = TableService()
    data = TableUpdate(password="new_pass")
    updated = await service.update_table(db_session, store.id, table.id, data)
    
    assert password_hasher.verify("new_pass", updated.password_hash)


@pytest.mark.asyncio
async def test_delete_table_success(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(store_id=store.id, table_number=1, password_hash="hash")
    db_session.add(table)
    await db_session.commit()
    table_id = table.id
    
    # Test
    service = TableService()
    await service.delete_table(db_session, store.id, table_id)
    
    # Verify deletion
    deleted = await service.table_repo.get_by_id(db_session, table_id)
    assert deleted is None


@pytest.mark.asyncio
async def test_delete_table_with_active_session_fails(db_session: AsyncSession):
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
    service = TableService()
    with pytest.raises(AppException) as exc_info:
        await service.delete_table(db_session, store.id, table.id)
    
    assert exc_info.value.code == "TABLE_HAS_ACTIVE_SESSION"


@pytest.mark.asyncio
async def test_complete_session(db_session: AsyncSession):
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
    
    # Test
    service = TableService()
    await service.complete_session(db_session, store.id, table.id)
    
    # Verify session is closed
    await db_session.refresh(session)
    assert session.is_active is False
    assert session.completed_at is not None


@pytest.mark.asyncio
async def test_get_table_dashboard(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table1 = Table(store_id=store.id, table_number=1, password_hash="hash")
    table2 = Table(store_id=store.id, table_number=2, password_hash="hash")
    db_session.add_all([table1, table2])
    await db_session.commit()
    
    session1 = TableSession(table_id=table1.id, started_at=datetime.utcnow(), is_active=True)
    db_session.add(session1)
    await db_session.commit()
    
    order = Order(
        session_id=session1.id,
        order_number="20260204-001",
        status=OrderStatus.PENDING,
        total_amount=15000
    )
    db_session.add(order)
    await db_session.commit()
    
    # Test
    service = TableService()
    dashboard = await service.get_table_dashboard(db_session, store.id)
    
    assert len(dashboard) == 2
    # Table 1 has active session with order
    table1_data = next(t for t in dashboard if t["table_number"] == 1)
    assert table1_data["is_active"] is True
    assert table1_data["total_amount"] == 15000
    assert table1_data["order_count"] == 1
