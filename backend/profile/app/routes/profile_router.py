from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.model import  User
from core.session import get_db
from core.config import settings

# from auth.app.schemas import RegisterRequest, RegisterResponse, RegisterFilter,LoginRequest, LoginResponse, LoginFilter
# from auth.app.services.custom import hash_password, verify_password, create_user,create_access_token

profile_router = APIRouter(prefix="/api/auth", tags=["auth"])
import logging
logger = logging.getLogger("uvicorn.error") 

@profile_router.post("/me")
def get_me():
   pass