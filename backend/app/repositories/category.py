from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)
    
    async def get_by_store(self, db: AsyncSession, store_id: int) -> List[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.store_id == store_id)
            .order_by(Category.display_order, Category.id)
        )
        return list(result.scalars().all())
    
    async def get_by_name(self, db: AsyncSession, store_id: int, name: str) -> Optional[Category]:
        result = await db.execute(
            select(Category).where(
                Category.store_id == store_id,
                Category.name == name
            )
        )
        return result.scalar_one_or_none()
