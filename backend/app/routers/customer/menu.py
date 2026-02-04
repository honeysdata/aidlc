from fastapi import APIRouter

from app.routers.dependencies import DbSession, TableToken
from app.schemas.menu import MenuListResponse, MenuResponse
from app.schemas.category import CategoryListResponse
from app.services.menu import MenuService
from app.services.category import CategoryService

router = APIRouter(prefix="/menu", tags=["Customer Menu"])


@router.get("/categories", response_model=CategoryListResponse)
async def get_categories(
    db: DbSession,
    token: TableToken
):
    """카테고리 목록 조회"""
    service = CategoryService()
    categories = await service.get_categories_by_store(db, token.store_id)
    return CategoryListResponse(categories=categories)


@router.get("", response_model=MenuListResponse)
async def get_menus(
    db: DbSession,
    token: TableToken
):
    """메뉴 목록 조회 (판매 가능한 메뉴만)"""
    service = MenuService()
    menus = await service.get_menus_by_store(db, token.store_id)
    return MenuListResponse(menus=menus)


@router.get("/category/{category_id}", response_model=MenuListResponse)
async def get_menus_by_category(
    category_id: int,
    db: DbSession,
    token: TableToken
):
    """카테고리별 메뉴 조회"""
    service = MenuService()
    menus = await service.get_menus_by_category(db, category_id)
    return MenuListResponse(menus=menus)


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    db: DbSession,
    token: TableToken
):
    """메뉴 상세 조회"""
    service = MenuService()
    return await service.get_menu_by_id(db, token.store_id, menu_id)
