from typing import Annotated, Optional
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import TokenPayload
from app.utils.jwt import jwt_handler
from app.utils.errors import AppException


async def get_table_token(
    authorization: Annotated[Optional[str], Header()] = None
) -> TokenPayload:
    """테이블 토큰 검증"""
    if not authorization or not authorization.startswith("Bearer "):
        raise AppException(
            code="UNAUTHORIZED",
            message="인증이 필요합니다",
            status_code=401
        )
    
    token = authorization.replace("Bearer ", "")
    return jwt_handler.verify_token(token, "table")


async def get_admin_token(
    authorization: Annotated[Optional[str], Header()] = None
) -> TokenPayload:
    """관리자 토큰 검증"""
    if not authorization or not authorization.startswith("Bearer "):
        raise AppException(
            code="UNAUTHORIZED",
            message="인증이 필요합니다",
            status_code=401
        )
    
    token = authorization.replace("Bearer ", "")
    return jwt_handler.verify_token(token, "admin")


# Type aliases for dependency injection
DbSession = Annotated[AsyncSession, Depends(get_db)]
TableToken = Annotated[TokenPayload, Depends(get_table_token)]
AdminToken = Annotated[TokenPayload, Depends(get_admin_token)]
