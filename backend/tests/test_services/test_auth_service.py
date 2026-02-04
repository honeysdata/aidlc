import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Store, User, Table, TableSession
from app.services.auth import AuthService
from app.utils.password import password_hasher
from app.utils.errors import AppException


@pytest.mark.asyncio
async def test_login_table_success(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    password = "1234"
    table = Table(
        store_id=store.id,
        table_number=1,
        password_hash=password_hasher.hash(password)
    )
    db_session.add(table)
    await db_session.commit()
    
    # Test
    service = AuthService()
    result = await service.login_table(db_session, "test-store", 1, password)
    
    assert result.token is not None
    assert result.store_id == "test-store"
    assert result.table_number == 1
    assert result.session_id is not None


@pytest.mark.asyncio
async def test_login_table_wrong_password(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    table = Table(
        store_id=store.id,
        table_number=1,
        password_hash=password_hasher.hash("1234")
    )
    db_session.add(table)
    await db_session.commit()
    
    # Test
    service = AuthService()
    with pytest.raises(AppException) as exc_info:
        await service.login_table(db_session, "test-store", 1, "wrong")
    
    assert exc_info.value.code == "AUTH_FAILED"


@pytest.mark.asyncio
async def test_login_table_store_not_found(db_session: AsyncSession):
    service = AuthService()
    with pytest.raises(AppException) as exc_info:
        await service.login_table(db_session, "nonexistent", 1, "1234")
    
    assert exc_info.value.code == "NOT_FOUND"


@pytest.mark.asyncio
async def test_login_admin_success(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    password = "admin1234"
    user = User(
        store_id=store.id,
        username="admin",
        password_hash=password_hasher.hash(password)
    )
    db_session.add(user)
    await db_session.commit()
    
    # Test
    service = AuthService()
    result = await service.login_admin(db_session, "test-store", "admin", password)
    
    assert result.token is not None
    assert result.store_id == "test-store"
    assert result.username == "admin"


@pytest.mark.asyncio
async def test_login_admin_wrong_password(db_session: AsyncSession):
    # Setup
    store = Store(store_id="test-store", name="테스트 매장")
    db_session.add(store)
    await db_session.commit()
    
    user = User(
        store_id=store.id,
        username="admin",
        password_hash=password_hasher.hash("admin1234")
    )
    db_session.add(user)
    await db_session.commit()
    
    # Test
    service = AuthService()
    with pytest.raises(AppException) as exc_info:
        await service.login_admin(db_session, "test-store", "admin", "wrong")
    
    assert exc_info.value.code == "AUTH_FAILED"
