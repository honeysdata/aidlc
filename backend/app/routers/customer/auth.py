from fastapi import APIRouter

from app.routers.dependencies import DbSession, TableToken
from app.schemas.auth import TableLoginRequest, TableLoginResponse
from app.services.auth import AuthService
from app.repositories.table import TableSessionRepository

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


@router.get("/session/check")
async def check_session(
    db: DbSession,
    token: TableToken
):
    """세션 유효성 확인"""
    session_repo = TableSessionRepository()
    session = await session_repo.get_by_id(db, token.session_id)
    
    if not session or not session.is_active:
        return {"valid": False, "message": "세션이 종료되었습니다"}
    
    return {"valid": True}
