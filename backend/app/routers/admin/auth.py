from fastapi import APIRouter

from app.routers.dependencies import DbSession
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Admin Auth"])


@router.post("/login", response_model=AdminLoginResponse)
async def login_admin(
    request: AdminLoginRequest,
    db: DbSession
):
    """관리자 로그인"""
    service = AuthService()
    return await service.login_admin(
        db,
        request.store_id,
        request.username,
        request.password
    )
