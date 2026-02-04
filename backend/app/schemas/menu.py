from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class MenuBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: int = Field(..., ge=0)
    description: Optional[str] = None
    category_id: int
    display_order: int = Field(default=0)
    is_available: bool = Field(default=True)
    
    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("메뉴명은 비어있을 수 없습니다")
        return v.strip()


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    category_id: Optional[int] = None
    display_order: Optional[int] = None
    is_available: Optional[bool] = None


class MenuResponse(BaseModel):
    id: int
    name: str
    price: int
    description: Optional[str]
    category_id: int
    display_order: int
    is_available: bool
    
    class Config:
        from_attributes = True


class MenuListResponse(BaseModel):
    menus: List[MenuResponse]
