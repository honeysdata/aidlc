from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin


class Table(Base, TimestampMixin):
    __tablename__ = "tables"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="tables")
    sessions = relationship("TableSession", back_populates="table", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("store_id", "table_number", name="uq_store_table_number"),
    )


class TableSession(Base):
    __tablename__ = "table_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    table = relationship("Table", back_populates="sessions")
    orders = relationship("Order", back_populates="session", cascade="all, delete-orphan")
    
    __table_args__ = (
        # 테이블당 활성 세션은 하나만 허용 (partial unique index)
        Index(
            "uq_table_active_session",
            "table_id",
            unique=True,
            postgresql_where=(is_active == True)
        ),
    )
