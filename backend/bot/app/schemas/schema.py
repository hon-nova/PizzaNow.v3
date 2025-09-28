import uuid
from core.session import Base

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
class Pizza(Base):
   __tablename__ = "pizzas"

   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String, nullable=False)
   description = Column(Text)
   full_price = Column(Numeric, nullable=False)
   slice_price = Column(Numeric, nullable=False)
   image_url = Column(String, nullable=False)
   ingredient_list=Column(ARRAY(String), nullable=False)
   type=Column(String,nullable=False)