from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.menu import Menu
from app.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    def __init__(self):
        super().__init__(Menu)
    
    async def get_by_store(self, db: AsyncSession, store_id: int) -> List[Menu]:
        result = await db.execute(
            select(Menu)
            .where(Menu.store_id == store_id, Menu.is_available == True)
            .order_by(Menu.display_order, Menu.id)
        )
        return list(result.scalars().all())
    
    async def get_by_category(self, db: AsyncSession, category_id: int) -> List[Menu]:
        result = await db.execute(
            select(Menu)
            .where(Menu.category_id == category_id, Menu.is_available == True)
            .order_by(Menu.display_order, Menu.id)
        )
        return list(result.scalars().all())
    
    async def get_all_by_store(self, db: AsyncSession, store_id: int) -> List[Menu]:
        """Get all menus including unavailable ones (for admin)"""
        result = await db.execute(
            select(Menu)
            .where(Menu.store_id == store_id)
            .order_by(Menu.display_order, Menu.id)
        )
        return list(result.scalars().all())
