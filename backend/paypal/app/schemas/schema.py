from decimal import Decimal
from pydantic import BaseModel
from typing import List, Union


class OrderRequest(BaseModel):
   amount: Union[float,str]

class OrderItemSchema(BaseModel):
   pizza_id: str
   quantity: int
   subAmount: float

class OrderCreateRequest(BaseModel):
   user_id: str
   cart_items: List[OrderItemSchema]
   discount: float = 0
   shipping_fee: float = 0
   taxes: float = 0
   total: float
   

 




