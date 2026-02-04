from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_name: str
    unit_price: int
    quantity: int
    subtotal: int
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: OrderStatus
    total_amount: int
    items: List[OrderItemResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderHistoryResponse(BaseModel):
    id: int
    order_number: str
    items_json: str  # JSON 문자열로 저장됨
    total_amount: int
    ordered_at: datetime
    completed_at: datetime
    
    class Config:
        from_attributes = True
    
    @property
    def items(self) -> List[dict]:
        import json
        return json.loads(self.items_json)


class OrderHistoryListResponse(BaseModel):
    orders: List[OrderHistoryResponse]
