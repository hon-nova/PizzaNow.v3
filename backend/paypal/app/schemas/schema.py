from decimal import Decimal
from pydantic import BaseModel
from typing import List, Union


class OrderRequest(BaseModel):
   amount: Union[float,str]

class OrderItemSchema(BaseModel):
   pizza_id: str
   quantity: int
   sub_amount: float

class OrderCreateRequest(BaseModel):
   user_id: str   
   paypal_order_id: str
   cart_items: List[OrderItemSchema]
   discount: float = 0
   shipping_fee: float = 0
   taxes: float = 0
   total: float

from paypal.app.models import Order
from uuid import UUID

class OrderItemOut(BaseModel):
   pizza_id: UUID
   quantity: int
   sub_amount: float
   
   model_config = {
   "from_attributes": True
}
 
from datetime import datetime   
class OrderOut(BaseModel):   
   id: UUID
   user_id: UUID
   paypal_order_id: str | None
   discount: float
   shipping_fee: float
   taxes: float
   total: float
   transaction_date: datetime
   shipment_status: str
   items: List[OrderItemOut] = []
   model_config = {
      "from_attributes": True
   }



   

 




