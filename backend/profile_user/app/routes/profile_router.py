from fastapi import APIRouter,Depends

from core.auth import get_current_user
from core.model import User
from profile_user.app.schemas import LoginFilter

profile_router = APIRouter(prefix="/api/auth", tags=["auth"])
import logging
logger = logging.getLogger("uvicorn.error") 

# curr_user = get_current_user()
# logging.info(f"curr_user: {curr_user}")

@profile_router.get("/me",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   logging.info(f"current user in /me route: {user.username}")
   base= LoginFilter.model_validate(user)
   # user_dict = base.model_dump()
   
   return base