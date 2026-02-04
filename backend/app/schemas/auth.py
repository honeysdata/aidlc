from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TableLoginRequest(BaseModel):
    store_id: str = Field(..., min_length=1, max_length=50)
    table_number: int = Field(..., ge=1)
    password: str = Field(..., min_length=4)


class TableLoginResponse(BaseModel):
    token: str
    store_id: str
    table_number: int
    session_id: int


class AdminLoginRequest(BaseModel):
    store_id: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=4)


class AdminLoginResponse(BaseModel):
    token: str
    store_id: str
    username: str
    expires_at: datetime


class TokenPayload(BaseModel):
    sub: str
    token_type: str
    store_id: int
    exp: datetime
    
    # Table token specific
    table_id: Optional[int] = None
    table_number: Optional[int] = None
    session_id: Optional[int] = None
    
    # Admin token specific
    user_id: Optional[int] = None
    username: Optional[str] = None
