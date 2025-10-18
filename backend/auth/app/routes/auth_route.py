from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.model import  User
from core.session import get_db
from core.config import settings


from auth.app.schemas import RegisterRequest, RegisterResponse, RegisterFilter,LoginRequest, LoginResponse, LoginFilter
from auth.app.services.custom import hash_password, verify_password, create_user, create_access_token


auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
import logging
logger = logging.getLogger("uvicorn.error") 

@auth_router.post("/register")
def register(payload: RegisterRequest,db: Session = Depends(get_db)) -> RegisterResponse |dict:
   try:
      # 1 check if user exists
      user_db = db.query(User).filter(User.email == payload.email).first()
      if user_db:
         return {
            "detail":"Username or email already exists. Log in instead."
         }       
      # 2. validate user inputs     
      create_user(**payload.model_dump()) # make it a dict
      
      # 3. insert user into DB
      hashed_pwd = hash_password(payload.password)
      
      new_user = User(
         username=payload.username,
         email = payload.email,
         password=hashed_pwd
         )
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
            
      base = RegisterFilter.model_validate(new_user)
      data = base.model_dump() #a dict
      data['message'] = "Registered successfully!"
      response = RegisterResponse(**data)     
      
      print(f"@auth_route register response: {response}")

      return response        
      
   except HTTPException:       
      raise
   except Exception as e:
        # Only log unexpected errors
      print(f"EXCEPTION /register: {str(e)}")
      raise HTTPException(status_code=500, detail=f"Exception: {str(e)}, Internal server error")
   
@auth_router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
   try:
      # 1 check if user exists
      user_db = db.query(User).filter(User.email == payload.email).first()
      logging.error(f"user_db: {user_db}")
      if not user_db:
         return {
            "detail":"User Not Found!"
         } 
      logging.error(f"Trying to verify password. plain_pwd={repr(payload.password)}, hashed_pwd={repr(user_db.password)}")
        
      if not verify_password(payload.password,user_db.password):
         return {
            "detail": "Password is incorrect!"
         }
              
      base = LoginFilter.model_validate(user_db)
      data = base.model_dump()
      
      jwt_data =  {
         "sub":str(user_db.id),
         "username":user_db.username
      }
      
      access_token = create_access_token(jwt_data)
      
      data['token']=access_token
      data['message'] ="Login Success"
      
      from fastapi.encoders import jsonable_encoder    
      data = jsonable_encoder(data)  
      
      cookie_params = {
         "httponly": True,
         "samesite": "none",
         "secure": True,
         "max_age": 60*60*24*30
      }
      response.set_cookie(
         key="k8s_token",
         value=access_token,
         domain=".pizzanowai.studio",  # note the leading dot
         httponly=True,
         secure=True,
         samesite="none",
         max_age=60*60*24*30
      )
      response = JSONResponse(content=data)
      
      return response      
      
   except Exception as e:
      print(f"EXCEPTION /login: {str(e)}")
      raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# test only
@auth_router.get("/secretValue")
def get_config_value():   
   try:
      return {
         "AUTH":"yes",
         "GOOGLE_REDIRECT_URI":settings.GOOGLE_REDIRECT_URI,
         "L_REDIRECT_URI":settings.L_REDIRECT_URI,
         "DATABASE_URL": settings.DATABASE_URL,
         "PROJECT_ID": settings.PROJECT_ID,
         "SECRET_KEY": settings.SECRET_KEY
      }
   except Exception as e:
      print(f"EXCEPTION: {e}")