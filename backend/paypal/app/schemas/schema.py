from decimal import Decimal
from pydantic import BaseModel

class OrderRequest(BaseModel):
   amount: Decimal