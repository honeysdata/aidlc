from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Menu
from app.repositories.menu import MenuRepository
from app.repositories.category import CategoryRepository
from app.schemas.menu import MenuCreate, MenuUpdate
from app.utils.errors import AppException


class MenuService:
    def __init__(self):
        self.menu_repo = MenuRepository()
        self.category_repo = CategoryRepository()
    
    async def get_menus_by_store(self, db: AsyncSession, store_id: int) -> List[Menu]:
        """고객용: 판매 가능한 메뉴만 조회"""
        return await self.menu_repo.get_by_store(db, store_id)
    
    async def get_all_menus_by_store(self, db: AsyncSession, store_id: int) -> List[Menu]:
        """관리자용: 모든 메뉴 조회 (품절 포함)"""
        return await self.menu_repo.get_all_by_store(db, store_id)
    
    async def get_menus_by_category(self, db: AsyncSession, category_id: int) -> List[Menu]:
        """카테고리별 메뉴 조회"""
        return await self.menu_repo.get_by_category(db, category_id)
    
    async def get_menu_by_id(self, db: AsyncSession, store_id: int, menu_id: int) -> Menu:
        """메뉴 단건 조회"""
        menu = await self.menu_repo.get_by_id(db, menu_id)
        if not menu or menu.store_id != store_id:
            raise AppException(
                code="NOT_FOUND",
                message="메뉴를 찾을 수 없습니다",
                status_code=404
            )
        return menu
    
    async def create_menu(
        self,
        db: AsyncSession,
        store_id: int,
        data: MenuCreate
    ) -> Menu:
        """메뉴 생성"""
        # 카테고리 검증
        category = await self.category_repo.get_by_id(db, data.category_id)
        if not category or category.store_id != store_id:
            raise AppException(
                code="NOT_FOUND",
                message="카테고리를 찾을 수 없습니다",
                status_code=404
            )
        
        menu = Menu(
            store_id=store_id,
            category_id=data.category_id,
            name=data.name,
            price=data.price,
            description=data.description,
            display_order=data.display_order,
            is_available=data.is_available
        )
        
        return await self.menu_repo.create(db, menu)
    
    async def update_menu(
        self,
        db: AsyncSession,
        store_id: int,
        menu_id: int,
        data: MenuUpdate
    ) -> Menu:
        """메뉴 수정"""
        menu = await self.get_menu_by_id(db, store_id, menu_id)
        
        # 카테고리 변경 시 검증
        if data.category_id is not None:
            category = await self.category_repo.get_by_id(db, data.category_id)
            if not category or category.store_id != store_id:
                raise AppException(
                    code="NOT_FOUND",
                    message="카테고리를 찾을 수 없습니다",
                    status_code=404
                )
        
        update_data = data.model_dump(exclude_unset=True)
        return await self.menu_repo.update(db, menu, update_data)
    
    async def delete_menu(self, db: AsyncSession, store_id: int, menu_id: int) -> None:
        """메뉴 삭제"""
        menu = await self.get_menu_by_id(db, store_id, menu_id)
        await self.menu_repo.delete(db, menu)
