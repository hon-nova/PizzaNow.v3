import datetime
import uuid

from sqlalchemy import (  
   Integer,
   Column,   
   Numeric,
   ForeignKey,
   DateTime,
   String
  )
from sqlalchemy.dialects.postgresql import UUID
from core import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from enum import Enum as PyEnum
from sqlalchemy import Column, String

class ShipmentStatus(str, PyEnum):
   pending = "pending"
   succeeded = "succeeded"
   failed = "failed"


class Order(Base):
   __tablename__="orders"
   
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)    
   
   paypal_order_id = Column(String, unique=True, nullable=True)

   discount = Column(Numeric(10, 2), default=0)
   shipping_fee = Column(Numeric(10, 2), default=0)
   taxes = Column(Numeric(10, 2), default=0)
   total = Column(Numeric(10, 2), nullable=False)
      
   transaction_date = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))     
   shipment_status = Column(String, default=ShipmentStatus.pending.value)
  
   # relationship to order items
   items = relationship("OrderItem", back_populates="order")
   
class OrderItem(Base):
   __tablename__ = "order_items"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
   
   pizza_id = Column(UUID(as_uuid=True), ForeignKey("pizzas.id"), nullable=False)
   quantity = Column(Integer, nullable=False)
   sub_amount = Column(Numeric(10, 2), nullable=False)

   order = relationship("Order", back_populates="items")