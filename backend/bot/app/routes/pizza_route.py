from fastapi import APIRouter, Query
from app.services.pizza import get_all_pizzas
from sqlalchemy.orm import Session
from core import SessionLocal

pizza_router = APIRouter(prefix="/api", tags=["pizza"])
import logging
logger = logging.getLogger("uvicorn.error") 

@pizza_router.get("/pizzas")
def get_pizzas(page: int = Query(1), limit: int = Query(8)):
   db = SessionLocal()
   try:
      return get_all_pizzas(db, page, limit)
   finally:
      db.close()