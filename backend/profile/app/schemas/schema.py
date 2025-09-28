from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class LoginFilter(BaseModel):
   id: UUID
   username: str
   email: str
   is_active: bool
   role: str
   avatar: Optional[str]
   
   model_config = {
      "from_attributes": True
   }