from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.repositories.category import CategoryRepository
from app.repositories.menu import MenuRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.errors import AppException


class CategoryService:
    def __init__(self):
        self.category_repo = CategoryRepository()
        self.menu_repo = MenuRepository()
    
    async def get_categories_by_store(self, db: AsyncSession, store_id: int) -> List[Category]:
        """매장의 모든 카테고리 조회"""
        return await self.category_repo.get_by_store(db, store_id)
    
    async def get_category_by_id(self, db: AsyncSession, store_id: int, category_id: int) -> Category:
        """카테고리 단건 조회"""
        category = await self.category_repo.get_by_id(db, category_id)
        if not category or category.store_id != store_id:
            raise AppException(
                code="NOT_FOUND",
                message="카테고리를 찾을 수 없습니다",
                status_code=404
            )
        return category
    
    async def create_category(
        self,
        db: AsyncSession,
        store_id: int,
        data: CategoryCreate
    ) -> Category:
        """카테고리 생성"""
        # 중복 이름 검증
        existing = await self.category_repo.get_by_name(db, store_id, data.name)
        if existing:
            raise AppException(
                code="DUPLICATE",
                message="이미 존재하는 카테고리명입니다",
                status_code=400
            )
        
        category = Category(
            store_id=store_id,
            name=data.name,
            display_order=data.display_order
        )
        
        return await self.category_repo.create(db, category)
    
    async def update_category(
        self,
        db: AsyncSession,
        store_id: int,
        category_id: int,
        data: CategoryUpdate
    ) -> Category:
        """카테고리 수정"""
        category = await self.get_category_by_id(db, store_id, category_id)
        
        # 이름 변경 시 중복 검증
        if data.name is not None and data.name != category.name:
            existing = await self.category_repo.get_by_name(db, store_id, data.name)
            if existing:
                raise AppException(
                    code="DUPLICATE",
                    message="이미 존재하는 카테고리명입니다",
                    status_code=400
                )
        
        update_data = data.model_dump(exclude_unset=True)
        return await self.category_repo.update(db, category, update_data)
    
    async def delete_category(self, db: AsyncSession, store_id: int, category_id: int) -> None:
        """카테고리 삭제"""
        category = await self.get_category_by_id(db, store_id, category_id)
        
        # 메뉴 존재 여부 확인
        menus = await self.menu_repo.get_by_category(db, category_id)
        if menus:
            raise AppException(
                code="CATEGORY_HAS_MENUS",
                message="메뉴가 있는 카테고리는 삭제할 수 없습니다",
                status_code=400
            )
        
        await self.category_repo.delete(db, category)
