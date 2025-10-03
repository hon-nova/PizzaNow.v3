from decimal import Decimal
from pydantic import BaseModel
from typing import List, Union, Optional


class OrderRequest(BaseModel):
   amount: Union[float,str]

class OrderItemSchema(BaseModel):
   order_id: Optional[str] = None 
   pizza_id: str
   quantity: int
   sub_amount: float

"""
   order_data = {
        "user_id": payload["user_id"],
        "paypal_order_id": order_id,
        "payment_status":payload.get("payment_status",""),
        "discount": payload.get("discount", 0),
        "shipping_fee": payload.get("shipping_fee", 0),
        "taxes": payload.get("taxes", 0),
        "total": payload.get("total", 0),
        "items": payload["cart_items"],  # MUST exist
        "transaction_date": datetime.utcnow(),
    }
"""
class OrderCreateRequest(BaseModel):
   user_id: str   
   paypal_order_id: str
   payment_status:str
   items: List[OrderItemSchema]
   discount: float = 0
   shipping_fee: float = 0
   taxes: float = 0
   total: float

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



   

 




