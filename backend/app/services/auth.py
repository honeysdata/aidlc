from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TableSession
from app.repositories.store import StoreRepository
from app.repositories.user import UserRepository
from app.repositories.table import TableRepository, TableSessionRepository
from app.schemas.auth import TableLoginResponse, AdminLoginResponse
from app.utils.jwt import jwt_handler
from app.utils.password import password_hasher
from app.utils.errors import AppException
from app.config import get_settings

settings = get_settings()


class AuthService:
    def __init__(self):
        self.store_repo = StoreRepository()
        self.user_repo = UserRepository()
        self.table_repo = TableRepository()
        self.session_repo = TableSessionRepository()
    
    async def login_table(
        self,
        db: AsyncSession,
        store_id: str,
        table_number: int,
        password: str
    ) -> TableLoginResponse:
        """테이블 로그인 처리"""
        # 1. 매장 검증
        store = await self.store_repo.get_by_store_id(db, store_id)
        if not store:
            raise AppException(
                code="NOT_FOUND",
                message="매장을 찾을 수 없습니다",
                status_code=404
            )
        
        # 2. 테이블 검증
        table = await self.table_repo.get_by_table_number(db, store.id, table_number)
        if not table:
            raise AppException(
                code="NOT_FOUND",
                message="테이블을 찾을 수 없습니다",
                status_code=404
            )
        
        # 3. 비밀번호 검증
        if not password_hasher.verify(password, table.password_hash):
            raise AppException(
                code="AUTH_FAILED",
                message="비밀번호가 일치하지 않습니다",
                status_code=401
            )
        
        # 4. 활성 세션 확인 또는 새 세션 생성
        session = await self.session_repo.get_active_session(db, table.id)
        if not session:
            session = TableSession(
                table_id=table.id,
                started_at=datetime.utcnow(),
                is_active=True
            )
            db.add(session)
            await db.commit()
            await db.refresh(session)
        
        # 5. JWT 토큰 발급
        token = jwt_handler.create_table_token(
            store_id=store.id,
            table_id=table.id,
            table_number=table.table_number,
            session_id=session.id
        )
        
        return TableLoginResponse(
            token=token,
            store_id=store_id,
            table_number=table_number,
            session_id=session.id
        )
    
    async def login_admin(
        self,
        db: AsyncSession,
        store_id: str,
        username: str,
        password: str
    ) -> AdminLoginResponse:
        """관리자 로그인 처리"""
        # 1. 매장 검증
        store = await self.store_repo.get_by_store_id(db, store_id)
        if not store:
            raise AppException(
                code="NOT_FOUND",
                message="매장을 찾을 수 없습니다",
                status_code=404
            )
        
        # 2. 사용자 검증
        user = await self.user_repo.get_by_username(db, store.id, username)
        if not user:
            raise AppException(
                code="AUTH_FAILED",
                message="사용자명 또는 비밀번호가 일치하지 않습니다",
                status_code=401
            )
        
        # 3. 비밀번호 검증
        if not password_hasher.verify(password, user.password_hash):
            raise AppException(
                code="AUTH_FAILED",
                message="사용자명 또는 비밀번호가 일치하지 않습니다",
                status_code=401
            )
        
        # 4. JWT 토큰 발급
        token = jwt_handler.create_admin_token(
            store_id=store.id,
            user_id=user.id,
            username=user.username
        )
        
        expires_at = datetime.utcnow() + timedelta(hours=settings.jwt_admin_expire_hours)
        
        return AdminLoginResponse(
            token=token,
            store_id=store_id,
            username=username,
            expires_at=expires_at
        )
