from typing import List
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, OrderItem
from app.models.order import OrderStatus
from app.repositories.order import OrderRepository, OrderItemRepository
from app.repositories.menu import MenuRepository
from app.repositories.table import TableSessionRepository
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.utils.errors import AppException


# 유효한 상태 전이 정의
VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.PREPARING],
    OrderStatus.PREPARING: [OrderStatus.COMPLETED],
    OrderStatus.COMPLETED: [],
}


class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.item_repo = OrderItemRepository()
        self.menu_repo = MenuRepository()
        self.session_repo = TableSessionRepository()
    
    async def create_order(
        self,
        db: AsyncSession,
        store_id: int,
        session_id: int,
        data: OrderCreate
    ) -> Order:
        """주문 생성"""
        # 1. 세션 검증
        session = await self.session_repo.get_by_id(db, session_id)
        if not session or not session.is_active:
            raise AppException(
                code="SESSION_INVALID",
                message="유효하지 않은 세션입니다",
                status_code=400
            )
        
        # 2. 주문 번호 생성
        today = date.today()
        today_count = await self.order_repo.get_today_count(db, store_id, today)
        order_number = f"{today.strftime('%Y%m%d')}-{today_count + 1:03d}"
        
        # 3. 주문 항목 검증 및 생성
        items = []
        total_amount = 0
        
        for item_data in data.items:
            menu = await self.menu_repo.get_by_id(db, item_data.menu_id)
            if not menu or menu.store_id != store_id:
                raise AppException(
                    code="NOT_FOUND",
                    message=f"메뉴를 찾을 수 없습니다 (ID: {item_data.menu_id})",
                    status_code=404
                )
            
            if not menu.is_available:
                raise AppException(
                    code="MENU_UNAVAILABLE",
                    message=f"품절된 메뉴입니다: {menu.name}",
                    status_code=400
                )
            
            subtotal = menu.price * item_data.quantity
            total_amount += subtotal
            
            items.append({
                "menu_id": menu.id,
                "menu_name": menu.name,
                "unit_price": menu.price,
                "quantity": item_data.quantity,
                "subtotal": subtotal
            })
        
        # 4. 주문 생성
        order = Order(
            session_id=session_id,
            order_number=order_number,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            created_at=datetime.utcnow()
        )
        db.add(order)
        await db.flush()
        
        # 5. 주문 항목 생성
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                menu_id=item["menu_id"],
                menu_name=item["menu_name"],
                unit_price=item["unit_price"],
                quantity=item["quantity"],
                subtotal=item["subtotal"]
            )
            db.add(order_item)
        
        await db.commit()
        
        # 6. 주문 조회 (items 포함)
        return await self.order_repo.get_with_items(db, order.id)
    
    async def get_order_by_id(self, db: AsyncSession, store_id: int, order_id: int) -> Order:
        """주문 단건 조회"""
        order = await self.order_repo.get_with_items(db, order_id)
        if not order:
            raise AppException(
                code="NOT_FOUND",
                message="주문을 찾을 수 없습니다",
                status_code=404
            )
        
        # 매장 검증 (세션 -> 테이블 -> 매장)
        session = await self.session_repo.get_by_id(db, order.session_id)
        if not session:
            raise AppException(
                code="NOT_FOUND",
                message="주문을 찾을 수 없습니다",
                status_code=404
            )
        
        return order
    
    async def get_orders_by_session(self, db: AsyncSession, session_id: int) -> List[Order]:
        """세션별 주문 목록 조회"""
        return await self.order_repo.get_by_session(db, session_id)
    
    async def update_order_status(
        self,
        db: AsyncSession,
        store_id: int,
        order_id: int,
        data: OrderStatusUpdate
    ) -> Order:
        """주문 상태 변경"""
        order = await self.get_order_by_id(db, store_id, order_id)
        
        # 상태 전이 검증
        if data.status not in VALID_TRANSITIONS.get(order.status, []):
            raise AppException(
                code="INVALID_STATUS_TRANSITION",
                message=f"'{order.status.value}'에서 '{data.status.value}'로 변경할 수 없습니다",
                status_code=400
            )
        
        order.status = data.status
        await db.commit()
        await db.refresh(order)
        
        return order
    
    async def delete_order(self, db: AsyncSession, store_id: int, order_id: int) -> None:
        """주문 삭제"""
        order = await self.get_order_by_id(db, store_id, order_id)
        await self.order_repo.delete(db, order)
