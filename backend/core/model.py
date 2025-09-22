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
from sqlalchemy.orm import relationship
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