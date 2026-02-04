from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.table import Table, TableSession
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    def __init__(self):
        super().__init__(Table)
    
    async def get_by_table_number(self, db: AsyncSession, store_id: int, table_number: int) -> Optional[Table]:
        result = await db.execute(
            select(Table).where(
                Table.store_id == store_id,
                Table.table_number == table_number
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_store(self, db: AsyncSession, store_id: int) -> List[Table]:
        result = await db.execute(
            select(Table)
            .where(Table.store_id == store_id)
            .order_by(Table.table_number)
        )
        return list(result.scalars().all())


class TableSessionRepository(BaseRepository[TableSession]):
    def __init__(self):
        super().__init__(TableSession)
    
    async def get_active_session(self, db: AsyncSession, table_id: int) -> Optional[TableSession]:
        result = await db.execute(
            select(TableSession).where(
                TableSession.table_id == table_id,
                TableSession.is_active == True
            )
        )
        return result.scalar_one_or_none()
    
    async def end_session(self, db: AsyncSession, session: TableSession) -> TableSession:
        from datetime import datetime
        session.is_active = False
        session.completed_at = datetime.utcnow()
        await db.commit()
        await db.refresh(session)
        return session
