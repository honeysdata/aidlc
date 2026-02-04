import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.routers.dependencies import DbSession, TableToken
from app.schemas.order import OrderCreate, OrderResponse, OrderListResponse
from app.services.order import OrderService
from app.services.sse import sse_manager

router = APIRouter(prefix="/orders", tags=["Customer Order"])


@router.post("", response_model=OrderResponse)
async def create_order(
    request: OrderCreate,
    db: DbSession,
    token: TableToken
):
    """주문 생성"""
    service = OrderService()
    order = await service.create_order(
        db,
        token.store_id,
        token.session_id,
        request
    )
    
    # SSE 알림 (관리자에게)
    await sse_manager.notify_new_order(
        token.store_id,
        {
            "order_id": order.id,
            "order_number": order.order_number,
            "table_number": token.table_number,
            "items": [
                {
                    "menu_name": item.menu_name,
                    "quantity": item.quantity,
                    "subtotal": item.subtotal
                }
                for item in order.items
            ],
            "total_amount": order.total_amount,
            "status": order.status.value,
            "created_at": order.created_at.isoformat()
        }
    )
    
    return order


@router.get("", response_model=OrderListResponse)
async def get_orders(
    db: DbSession,
    token: TableToken
):
    """현재 세션의 주문 목록 조회"""
    service = OrderService()
    orders = await service.get_orders_by_session(db, token.session_id)
    return OrderListResponse(orders=orders)


@router.get("/stream")
async def stream_orders(
    token: TableToken
):
    """주문 상태 실시간 스트림 (SSE)"""
    async def event_generator():
        queue = await sse_manager.connect_customer(token.session_id)
        try:
            # 연결 확인 이벤트
            yield "event: connected\ndata: {}\n\n"
            
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield event.format()
                except asyncio.TimeoutError:
                    # Keep-alive
                    yield ": heartbeat\n\n"
        finally:
            await sse_manager.disconnect_customer(token.session_id, queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
