import asyncio
import json
from typing import Dict, Set
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SSEEvent:
    event_type: str
    data: dict
    
    def format(self) -> str:
        """SSE 형식으로 포맷팅"""
        return f"event: {self.event_type}\ndata: {json.dumps(self.data, ensure_ascii=False, default=str)}\n\n"


class SSEManager:
    """Server-Sent Events 관리자"""
    
    def __init__(self):
        # store_id -> set of queues (admin connections)
        self._admin_connections: Dict[int, Set[asyncio.Queue]] = {}
        # session_id -> set of queues (customer connections)
        self._customer_connections: Dict[int, Set[asyncio.Queue]] = {}
    
    async def connect_admin(self, store_id: int) -> asyncio.Queue:
        """관리자 SSE 연결"""
        queue = asyncio.Queue()
        
        if store_id not in self._admin_connections:
            self._admin_connections[store_id] = set()
        
        self._admin_connections[store_id].add(queue)
        return queue
    
    async def disconnect_admin(self, store_id: int, queue: asyncio.Queue) -> None:
        """관리자 SSE 연결 해제"""
        if store_id in self._admin_connections:
            self._admin_connections[store_id].discard(queue)
            if not self._admin_connections[store_id]:
                del self._admin_connections[store_id]
    
    async def connect_customer(self, session_id: int) -> asyncio.Queue:
        """고객 SSE 연결"""
        queue = asyncio.Queue()
        
        if session_id not in self._customer_connections:
            self._customer_connections[session_id] = set()
        
        self._customer_connections[session_id].add(queue)
        return queue
    
    async def disconnect_customer(self, session_id: int, queue: asyncio.Queue) -> None:
        """고객 SSE 연결 해제"""
        if session_id in self._customer_connections:
            self._customer_connections[session_id].discard(queue)
            if not self._customer_connections[session_id]:
                del self._customer_connections[session_id]
    
    async def broadcast_to_admin(self, store_id: int, event: SSEEvent) -> None:
        """관리자에게 이벤트 브로드캐스트"""
        if store_id not in self._admin_connections:
            return
        
        for queue in self._admin_connections[store_id]:
            await queue.put(event)
    
    async def broadcast_to_customer(self, session_id: int, event: SSEEvent) -> None:
        """고객에게 이벤트 브로드캐스트"""
        if session_id not in self._customer_connections:
            return
        
        for queue in self._customer_connections[session_id]:
            await queue.put(event)
    
    async def notify_new_order(self, store_id: int, order_data: dict) -> None:
        """새 주문 알림 (관리자에게)"""
        event = SSEEvent(
            event_type="new_order",
            data=order_data
        )
        await self.broadcast_to_admin(store_id, event)
    
    async def notify_order_updated(
        self,
        store_id: int,
        session_id: int,
        order_id: int,
        status: str
    ) -> None:
        """주문 상태 변경 알림 (관리자 + 고객)"""
        event = SSEEvent(
            event_type="order_updated",
            data={
                "order_id": order_id,
                "status": status
            }
        )
        await self.broadcast_to_admin(store_id, event)
        await self.broadcast_to_customer(session_id, event)
    
    async def notify_order_deleted(
        self,
        store_id: int,
        session_id: int,
        order_id: int
    ) -> None:
        """주문 삭제 알림 (관리자 + 고객)"""
        event = SSEEvent(
            event_type="order_deleted",
            data={
                "order_id": order_id
            }
        )
        await self.broadcast_to_admin(store_id, event)
        await self.broadcast_to_customer(session_id, event)
    
    async def notify_session_completed(
        self,
        store_id: int,
        session_id: int
    ) -> None:
        """세션 완료 알림 (고객에게) - 이용 완료 시"""
        event = SSEEvent(
            event_type="session_completed",
            data={
                "session_id": session_id,
                "message": "이용이 완료되었습니다"
            }
        )
        await self.broadcast_to_customer(session_id, event)


# 싱글톤 인스턴스
sse_manager = SSEManager()
