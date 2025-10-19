from fastapi import APIRouter,Depends

from core.auth import get_current_user
from core.model import User
from core.schema import LoginFilter

profile_router = APIRouter(prefix="/api/profile", tags=["auth"])
import logging
logger = logging.getLogger("uvicorn.error") 


@profile_router.get("/me",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   logging.info(f"current user in /me route: {user.username}")
   base= LoginFilter.model_validate(user)
   
   return base

from core.config import settings
# test only
@profile_router.get("/secretValue")
def get_config_value():   
   try:
      return {
         "PROFILE":"yes",
         "GOOGLE_REDIRECT_URI":settings.GOOGLE_REDIRECT_URI,
         "L_REDIRECT_URI":settings.L_REDIRECT_URI,
         "DATABASE_URL": settings.DATABASE_URL,
         "PROJECT_ID": settings.PROJECT_ID,
         "SECRET_KEY": settings.SECRET_KEY
      }
   except Exception as e:
      print(f"EXCEPTION: {e}")

