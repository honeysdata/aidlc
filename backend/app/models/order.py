from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base, TimestampMixin
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("table_sessions.id"), nullable=False)
    order_number = Column(String(20), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = Column(Integer, nullable=False)
    
    # Relationships
    session = relationship("TableSession", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=True)  # Nullable for snapshot
    menu_name = Column(String(100), nullable=False)  # Snapshot
    unit_price = Column(Integer, nullable=False)  # Snapshot
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")


class OrderHistory(Base):
    __tablename__ = "order_history"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    order_number = Column(String(20), nullable=False)
    items_json = Column(JSON, nullable=False)
    total_amount = Column(Integer, nullable=False)
    ordered_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, server_default=func.now(), nullable=False)
