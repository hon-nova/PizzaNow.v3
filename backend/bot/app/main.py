import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.model import User
from bot.app.routes import bot_router,graph_router
# from core.session import SessionLocal
from bot.app.services import respond_shipment_status

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() 

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
) 
    
# app.include_router(test_router, prefix="/test") 
app.include_router(bot_router) 
app.include_router(graph_router) 

# if settings.ENV.upper()=="DEV":
#    Base.metadata.create_all(bind=engine)
print(f"RESPOND_SHIPMENT_STATUS")
print(respond_shipment_status("591c1973-8e02-4a29-a30c-905fe720ab58"))

@app.get("/bot-ping")
def ping():
   return {"8082": "pong"}
   
if __name__ == "__main__":
   

   port = int(os.environ.get("PORT", 8082))
   import uvicorn
   uvicorn.run("bot.app.main:app", host="0.0.0.0", port=port)


   
