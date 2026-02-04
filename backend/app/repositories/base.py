from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[T]:
        return await db.get(self.model, id)
    
    # Alias for get
    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[T]:
        return await self.get(db, id)
    
    async def get_all(self, db: AsyncSession) -> List[T]:
        result = await db.execute(select(self.model))
        return list(result.scalars().all())
    
    async def create(self, db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def update(self, db: AsyncSession, obj: T) -> T:
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def delete(self, db: AsyncSession, obj: T) -> bool:
        await db.delete(obj)
        await db.commit()
        return True
