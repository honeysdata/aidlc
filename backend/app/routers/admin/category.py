from fastapi import APIRouter

from app.routers.dependencies import DbSession, AdminToken
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Admin Category"])


@router.get("", response_model=CategoryListResponse)
async def get_categories(
    db: DbSession,
    token: AdminToken
):
    """카테고리 목록 조회"""
    service = CategoryService()
    categories = await service.get_categories_by_store(db, token.store_id)
    return CategoryListResponse(categories=categories)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: DbSession,
    token: AdminToken
):
    """카테고리 상세 조회"""
    service = CategoryService()
    return await service.get_category_by_id(db, token.store_id, category_id)


@router.post("", response_model=CategoryResponse)
async def create_category(
    request: CategoryCreate,
    db: DbSession,
    token: AdminToken
):
    """카테고리 생성"""
    service = CategoryService()
    return await service.create_category(db, token.store_id, request)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: DbSession,
    token: AdminToken
):
    """카테고리 수정"""
    service = CategoryService()
    return await service.update_category(db, token.store_id, category_id, request)


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: DbSession,
    token: AdminToken
):
    """카테고리 삭제"""
    service = CategoryService()
    await service.delete_category(db, token.store_id, category_id)
    return {"message": "카테고리가 삭제되었습니다"}
