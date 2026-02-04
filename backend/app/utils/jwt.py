from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import get_settings
from app.schemas.auth import TokenPayload
from app.utils.errors import AppException

settings = get_settings()


class JWTHandler:
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.admin_expire_hours = settings.jwt_admin_expire_hours
        self.table_expire_hours = settings.jwt_table_expire_hours
    
    def create_table_token(
        self,
        store_id: int,
        table_id: int,
        table_number: int,
        session_id: int
    ) -> str:
        expire = datetime.utcnow() + timedelta(hours=self.table_expire_hours)
        payload = {
            "sub": f"table:{table_id}",
            "token_type": "table",
            "store_id": store_id,
            "table_id": table_id,
            "table_number": table_number,
            "session_id": session_id,
            "exp": expire
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_admin_token(
        self,
        store_id: int,
        user_id: int,
        username: str
    ) -> str:
        expire = datetime.utcnow() + timedelta(hours=self.admin_expire_hours)
        payload = {
            "sub": f"admin:{user_id}",
            "token_type": "admin",
            "store_id": store_id,
            "user_id": user_id,
            "username": username,
            "exp": expire
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("token_type") != token_type:
                raise AppException(
                    code="INVALID_TOKEN_TYPE",
                    message="잘못된 토큰 유형입니다",
                    status_code=401
                )
            
            return TokenPayload(
                sub=payload["sub"],
                token_type=payload["token_type"],
                store_id=payload["store_id"],
                exp=datetime.fromtimestamp(payload["exp"]),
                table_id=payload.get("table_id"),
                table_number=payload.get("table_number"),
                session_id=payload.get("session_id"),
                user_id=payload.get("user_id"),
                username=payload.get("username")
            )
        except JWTError:
            raise AppException(
                code="INVALID_TOKEN",
                message="유효하지 않은 토큰입니다",
                status_code=401
            )
    
    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise AppException(
                code="INVALID_TOKEN",
                message="유효하지 않은 토큰입니다",
                status_code=401
            )


jwt_handler = JWTHandler()
