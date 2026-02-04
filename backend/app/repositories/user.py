from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    async def get_by_username(self, db: AsyncSession, store_id: int, username: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(
                User.store_id == store_id,
                User.username == username
            )
        )
        return result.scalar_one_or_none()
