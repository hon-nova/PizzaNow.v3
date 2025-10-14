import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.session import Base, engine 
from profile_user.app.routes import profile_router


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
app.include_router(profile_router) 

# logging.info(f"DATABASE_URL CURRENTLY: {settings.DATABASE_URL}")
# logger.info("@main Routers: %s", app.routes)

# if settings.ENV.upper()=="DEV":
#    Base.metadata.create_all(bind=engine)

@app.get("/profileping")
def ping():
   return {"profileping": "profile-pong"}
   
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 8081))
   import uvicorn
   uvicorn.run("profile_user.app.main:app", host="0.0.0.0", port=port)


   
