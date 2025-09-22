from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class RegisterRequest(BaseModel):
   username: str
   email: str
   password: str
   confirm_password: str   

class RegisterFilter(BaseModel):
   id: UUID
   username: str
   email: str
   is_active: bool
   role: str
   avatar: Optional[str]
   
   model_config = {
      "from_attributes": True
   }  

class RegisterResponse(RegisterFilter):
   message: str

class LoginRequest(BaseModel):   
   email: str
   password: str

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
class LoginResponse(LoginFilter):
   message: str
