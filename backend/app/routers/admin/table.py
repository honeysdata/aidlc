from typing import Optional
from datetime import date
from fastapi import APIRouter, Query

from app.routers.dependencies import DbSession, AdminToken
from app.schemas.table import (
    TableCreate, TableUpdate, TableResponse, 
    TableListResponse, TableDashboardResponse, TableSessionResponse
)
from app.schemas.order import OrderHistoryListResponse
from app.services.table import TableService
from app.repositories.order import OrderHistoryRepository

router = APIRouter(prefix="/tables", tags=["Admin Table"])


@router.get("", response_model=TableListResponse)
async def get_tables(
    db: DbSession,
    token: AdminToken
):
    """테이블 목록 조회"""
    service = TableService()
    tables = await service.get_tables_by_store(db, token.store_id)
    return TableListResponse(tables=tables)


@router.get("/dashboard", response_model=TableDashboardResponse)
async def get_table_dashboard(
    db: DbSession,
    token: AdminToken
):
    """테이블 대시보드 (현황 조회)"""
    service = TableService()
    dashboard_data = await service.get_table_dashboard(db, token.store_id)
    
    tables = [
        TableSessionResponse(
            id=t["id"],
            table_number=t["table_number"],
            started_at=t["started_at"] or None,
            is_active=t["is_active"],
            total_amount=t["total_amount"],
            order_count=t["order_count"]
        )
        for t in dashboard_data
    ]
    
    return TableDashboardResponse(tables=tables)


@router.post("", response_model=TableResponse)
async def create_table(
    request: TableCreate,
    db: DbSession,
    token: AdminToken
):
    """테이블 생성"""
    service = TableService()
    return await service.create_table(db, token.store_id, request)


@router.patch("/{table_id}", response_model=TableResponse)
async def update_table(
    table_id: int,
    request: TableUpdate,
    db: DbSession,
    token: AdminToken
):
    """테이블 수정 (비밀번호 변경)"""
    service = TableService()
    return await service.update_table(db, token.store_id, table_id, request)


@router.delete("/{table_id}")
async def delete_table(
    table_id: int,
    db: DbSession,
    token: AdminToken
):
    """테이블 삭제"""
    service = TableService()
    await service.delete_table(db, token.store_id, table_id)
    return {"message": "테이블이 삭제되었습니다"}


@router.post("/{table_id}/complete")
async def complete_table_session(
    table_id: int,
    db: DbSession,
    token: AdminToken
):
    """이용 완료 처리"""
    service = TableService()
    await service.complete_session(db, token.store_id, table_id)
    return {"message": "이용 완료 처리되었습니다"}


@router.get("/{table_id}/history", response_model=OrderHistoryListResponse)
async def get_table_history(
    table_id: int,
    db: DbSession,
    token: AdminToken,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None)
):
    """테이블 과거 주문 내역 조회"""
    # 테이블 정보 조회
    service = TableService()
    table = await service.get_table_by_id(db, token.store_id, table_id)
    
    # 주문 내역 조회
    history_repo = OrderHistoryRepository()
    histories = await history_repo.get_by_table_and_date(
        db,
        token.store_id,
        table.table_number,
        date_from,
        date_to
    )
    
    return OrderHistoryListResponse(orders=histories)
