from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.store import Store
from app.repositories.base import BaseRepository


class StoreRepository(BaseRepository[Store]):
    def __init__(self):
        super().__init__(Store)
    
    async def get_by_store_id(self, db: AsyncSession, store_id: str) -> Optional[Store]:
        result = await db.execute(
            select(Store).where(Store.store_id == store_id)
        )
        return result.scalar_one_or_none()
