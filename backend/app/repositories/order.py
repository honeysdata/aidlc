from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem, OrderHistory
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)
    
    async def get_with_items(self, db: AsyncSession, order_id: int) -> Optional[Order]:
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_session(self, db: AsyncSession, session_id: int) -> List[Order]:
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.session_id == session_id)
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def get_today_count(self, db: AsyncSession, store_id: int, today: date) -> int:
        from app.models.table import TableSession, Table
        
        result = await db.execute(
            select(func.count(Order.id))
            .join(TableSession, Order.session_id == TableSession.id)
            .join(Table, TableSession.table_id == Table.id)
            .where(
                Table.store_id == store_id,
                func.date(Order.created_at) == today
            )
        )
        return result.scalar() or 0


class OrderItemRepository(BaseRepository[OrderItem]):
    def __init__(self):
        super().__init__(OrderItem)


class OrderHistoryRepository(BaseRepository[OrderHistory]):
    def __init__(self):
        super().__init__(OrderHistory)
    
    async def get_by_table_and_date(
        self,
        db: AsyncSession,
        store_id: int,
        table_number: int,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[OrderHistory]:
        query = select(OrderHistory).where(
            OrderHistory.store_id == store_id,
            OrderHistory.table_number == table_number
        )
        
        if date_from:
            query = query.where(func.date(OrderHistory.completed_at) >= date_from)
        if date_to:
            query = query.where(func.date(OrderHistory.completed_at) <= date_to)
        
        query = query.order_by(OrderHistory.completed_at.desc())
        
        result = await db.execute(query)
        return list(result.scalars().all())
