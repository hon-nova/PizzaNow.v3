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
)
from sqlalchemy.dialects.postgresql import UUID
from core import Base
class User(Base):
   __tablename__="users"
   
   id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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
 