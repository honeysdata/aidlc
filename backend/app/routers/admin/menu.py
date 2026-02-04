from fastapi import APIRouter

from app.routers.dependencies import DbSession, AdminToken
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse, MenuListResponse
from app.services.menu import MenuService

router = APIRouter(prefix="/menus", tags=["Admin Menu"])


@router.get("", response_model=MenuListResponse)
async def get_menus(
    db: DbSession,
    token: AdminToken
):
    """메뉴 목록 조회 (품절 포함)"""
    service = MenuService()
    menus = await service.get_all_menus_by_store(db, token.store_id)
    return MenuListResponse(menus=menus)


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    db: DbSession,
    token: AdminToken
):
    """메뉴 상세 조회"""
    service = MenuService()
    return await service.get_menu_by_id(db, token.store_id, menu_id)


@router.post("", response_model=MenuResponse)
async def create_menu(
    request: MenuCreate,
    db: DbSession,
    token: AdminToken
):
    """메뉴 생성"""
    service = MenuService()
    return await service.create_menu(db, token.store_id, request)


@router.patch("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    request: MenuUpdate,
    db: DbSession,
    token: AdminToken
):
    """메뉴 수정"""
    service = MenuService()
    return await service.update_menu(db, token.store_id, menu_id, request)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    db: DbSession,
    token: AdminToken
):
    """메뉴 삭제"""
    service = MenuService()
    await service.delete_menu(db, token.store_id, menu_id)
    return {"message": "메뉴가 삭제되었습니다"}
