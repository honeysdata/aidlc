from typing import List, Optional
from datetime import datetime
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Table, TableSession, Order, OrderHistory
from app.repositories.table import TableRepository, TableSessionRepository
from app.repositories.order import OrderRepository
from app.schemas.table import TableCreate, TableUpdate
from app.utils.password import password_hasher
from app.utils.errors import AppException


class TableService:
    def __init__(self):
        self.table_repo = TableRepository()
        self.session_repo = TableSessionRepository()
        self.order_repo = OrderRepository()
    
    async def get_tables_by_store(self, db: AsyncSession, store_id: int) -> List[Table]:
        """매장의 모든 테이블 조회"""
        return await self.table_repo.get_by_store(db, store_id)
    
    async def get_table_by_id(self, db: AsyncSession, store_id: int, table_id: int) -> Table:
        """테이블 단건 조회"""
        table = await self.table_repo.get_by_id(db, table_id)
        if not table or table.store_id != store_id:
            raise AppException(
                code="NOT_FOUND",
                message="테이블을 찾을 수 없습니다",
                status_code=404
            )
        return table
    
    async def get_active_session_id(self, db: AsyncSession, store_id: int, table_id: int) -> Optional[int]:
        """테이블의 활성 세션 ID 조회"""
        table = await self.get_table_by_id(db, store_id, table_id)
        session = await self.session_repo.get_active_session(db, table.id)
        return session.id if session else None
    
    async def create_table(
        self,
        db: AsyncSession,
        store_id: int,
        data: TableCreate
    ) -> Table:
        """테이블 생성"""
        # 중복 테이블 번호 검증
        existing = await self.table_repo.get_by_table_number(db, store_id, data.table_number)
        if existing:
            raise AppException(
                code="DUPLICATE",
                message="이미 존재하는 테이블 번호입니다",
                status_code=400
            )
        
        table = Table(
            store_id=store_id,
            table_number=data.table_number,
            password_hash=password_hasher.hash(data.password)
        )
        
        return await self.table_repo.create(db, table)
    
    async def update_table(
        self,
        db: AsyncSession,
        store_id: int,
        table_id: int,
        data: TableUpdate
    ) -> Table:
        """테이블 수정 (비밀번호 변경)"""
        table = await self.get_table_by_id(db, store_id, table_id)
        
        if data.password:
            table.password_hash = password_hasher.hash(data.password)
            await db.commit()
            await db.refresh(table)
        
        return table
    
    async def delete_table(self, db: AsyncSession, store_id: int, table_id: int) -> None:
        """테이블 삭제"""
        table = await self.get_table_by_id(db, store_id, table_id)
        
        # 활성 세션 확인
        active_session = await self.session_repo.get_active_session(db, table_id)
        if active_session:
            raise AppException(
                code="TABLE_HAS_ACTIVE_SESSION",
                message="활성 세션이 있는 테이블은 삭제할 수 없습니다",
                status_code=400
            )
        
        await self.table_repo.delete(db, table)
    
    async def complete_session(
        self,
        db: AsyncSession,
        store_id: int,
        table_id: int
    ) -> None:
        """이용 완료 처리 (세션 종료)"""
        table = await self.get_table_by_id(db, store_id, table_id)
        
        # 활성 세션 확인
        session = await self.session_repo.get_active_session(db, table_id)
        if not session:
            raise AppException(
                code="SESSION_NOT_FOUND",
                message="활성 세션이 없습니다",
                status_code=404
            )
        
        # 주문 조회
        orders = await self.order_repo.get_by_session(db, session.id)
        
        # 주문을 OrderHistory로 이동
        for order in orders:
            items_json = [
                {
                    "menu_name": item.menu_name,
                    "unit_price": item.unit_price,
                    "quantity": item.quantity,
                    "subtotal": item.subtotal
                }
                for item in order.items
            ]
            
            history = OrderHistory(
                store_id=store_id,
                table_number=table.table_number,
                session_id=session.id,
                order_number=order.order_number,
                items_json=json.dumps(items_json, ensure_ascii=False),
                total_amount=order.total_amount,
                ordered_at=order.created_at,
                completed_at=datetime.utcnow()
            )
            db.add(history)
            
            # 원본 주문 삭제
            await db.delete(order)
        
        # 세션 종료
        session.is_active = False
        session.completed_at = datetime.utcnow()
        
        await db.commit()
    
    async def get_table_dashboard(
        self,
        db: AsyncSession,
        store_id: int
    ) -> List[dict]:
        """테이블 대시보드 데이터 조회"""
        tables = await self.table_repo.get_by_store(db, store_id)
        
        result = []
        for table in tables:
            session = await self.session_repo.get_active_session(db, table.id)
            
            if session:
                orders = await self.order_repo.get_by_session(db, session.id)
                total_amount = sum(o.total_amount for o in orders)
                order_count = len(orders)
                
                result.append({
                    "id": table.id,
                    "table_number": table.table_number,
                    "session_id": session.id,
                    "started_at": session.started_at,
                    "is_active": True,
                    "total_amount": total_amount,
                    "order_count": order_count
                })
            else:
                result.append({
                    "id": table.id,
                    "table_number": table.table_number,
                    "session_id": None,
                    "started_at": None,
                    "is_active": False,
                    "total_amount": 0,
                    "order_count": 0
                })
        
        return result
