from fastapi import APIRouter, Query
from core.crud import get_all_pizzas
from core.session import SessionLocal

from core.auth import get_current_user
from fastapi import Depends
from core.model import User
from core.schema import LoginFilter
import logging
logger = logging.getLogger("uvicorn.error") 
bot_router = APIRouter(prefix="/api/bot", tags=["pizza"])

@bot_router.get("/pizzas")
def get_pizzas(page: int = Query(1), limit: int = Query(8)):
   db = SessionLocal()
   try:
      # logging.info(get_all_pizzas(db, page, limit))
      return get_all_pizzas(db, page, limit)
   finally:
      db.close() 


@bot_router.get("/auth",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   logging.info(f"bot user in /auth route: {user.username}")
   base= LoginFilter.model_validate(user)
   # user_dict = base.model_dump()
   
   return base

from core.config import settings
# test only
@bot_router.get("/secretValue")
def get_config_value():   
   try:
      return {
         "BOT":"yes",
         "AWS_ACCESS_KEY_ID":settings.AWS_ACCESS_KEY_ID,
         "AWS_S3_BUCKET":settings.AWS_S3_BUCKET,
          "VERTEX_REGION":settings.VERTEX_REGION,
         "DATABASE_URL": settings.DATABASE_URL,
         
      }
   except Exception as e:
      print(f"EXCEPTION: {e}")
   