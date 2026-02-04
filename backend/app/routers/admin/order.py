import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.routers.dependencies import DbSession, AdminToken
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.services.order import OrderService
from app.services.sse import sse_manager

router = APIRouter(prefix="/orders", tags=["Admin Order"])


@router.get("/stream")
async def stream_orders(
    token: AdminToken
):
    """주문 실시간 스트림 (SSE)"""
    async def event_generator():
        queue = await sse_manager.connect_admin(token.store_id)
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
            await sse_manager.disconnect_admin(token.store_id, queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    request: OrderStatusUpdate,
    db: DbSession,
    token: AdminToken
):
    """주문 상태 변경"""
    service = OrderService()
    order = await service.update_order_status(
        db,
        token.store_id,
        order_id,
        request
    )
    
    # SSE 알림 (관리자 + 고객)
    await sse_manager.notify_order_updated(
        token.store_id,
        order.session_id,
        order.id,
        order.status.value
    )
    
    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: DbSession,
    token: AdminToken
):
    """주문 삭제"""
    service = OrderService()
    
    # 삭제 전 세션 ID 조회
    order = await service.get_order_by_id(db, token.store_id, order_id)
    session_id = order.session_id
    
    await service.delete_order(db, token.store_id, order_id)
    
    # SSE 알림 (관리자 + 고객)
    await sse_manager.notify_order_deleted(
        token.store_id,
        session_id,
        order_id
    )
    
    return {"message": "주문이 삭제되었습니다"}
