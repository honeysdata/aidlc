from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class TableBase(BaseModel):
    table_number: int = Field(..., ge=1)


class TableCreate(TableBase):
    password: str = Field(..., min_length=4)


class TableUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=4)


class TableResponse(TableBase):
    id: int
    
    class Config:
        from_attributes = True


class TableListResponse(BaseModel):
    tables: List[TableResponse]


class TableSessionResponse(BaseModel):
    id: int
    table_number: int
    session_id: Optional[int] = None
    started_at: Optional[datetime] = None
    is_active: bool
    total_amount: int = 0
    order_count: int = 0


class TableDashboardResponse(BaseModel):
    tables: List[TableSessionResponse]
