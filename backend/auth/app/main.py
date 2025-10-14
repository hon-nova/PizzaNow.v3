import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from auth.app.routes import auth_router,auth_google_router,auth_linkedin_router
from core.model import User

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
app.include_router(auth_router) 
app.include_router(auth_google_router) 
app.include_router(auth_linkedin_router) 


@app.get("/authping")
def ping():
   return {"authping": "auth-pong"}
   
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 8000))
   import uvicorn
   uvicorn.run("auth.app.main:app", host="0.0.0.0", port=port)


   
