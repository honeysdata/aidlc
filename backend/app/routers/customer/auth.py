from fastapi import APIRouter

from app.routers.dependencies import DbSession
from app.schemas.auth import TableLoginRequest, TableLoginResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Customer Auth"])


@router.post("/login", response_model=TableLoginResponse)
async def login_table(
    request: TableLoginRequest,
    db: DbSession
):
    """테이블 로그인"""
    service = AuthService()
    return await service.login_table(
        db,
        request.store_id,
        request.table_number,
        request.password
    )
