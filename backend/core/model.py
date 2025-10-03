import uuid
from sqlalchemy import (
   Boolean,
   Integer,
   Column,
   String,
   Text,
   Numeric,
   ForeignKey,
   ARRAY,
   DateTime   
)
from sqlalchemy.dialects.postgresql import UUID
from core import Base
import datetime
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum

class User(Base):
   __tablename__="users"   
   
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   username=Column(String, unique=True)
   email=Column(String,unique=True)
   password=Column(String)
   role=Column(String, default="user")
   is_active = Column(Boolean, default=False)
   avatar = Column(String)
   provider=Column(String, default="custom")
   provider_id= Column(String)

class Pizza(Base):
   __tablename__ = 'pizzas'

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   name = Column(String, nullable=False)
   description = Column(Text)
   full_price = Column(Numeric, nullable=False)
   slice_price = Column(Numeric, nullable=False)
   image_url = Column(String, nullable=False)
   ingredients = Column(ARRAY(String),nullable=False)
   pizza_type =  Column(String, nullable=False)
   


class ShipmentStatus(str, PyEnum):
   pending = "pending"
   succeeded = "succeeded"
   failed = "failed"


class Order(Base):
   __tablename__="orders"
   
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)    
   
   paypal_order_id = Column(String, unique=True, nullable=True)
   payment_status = Column(String,nullable=False,default="PENDING")

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
 