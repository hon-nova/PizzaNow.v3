from sqlalchemy.orm import Session
from core.model import User
import logging
from fastapi import HTTPException, Depends
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests  # used ONLY for id_token verification
from core import get_db

logger = logging.getLogger("uvicorn.error")

def save_google_user_to_db(id_token_string:str,db: Session = Depends(get_db)):
   try:      
      idinfo = id_token.verify_oauth2_token(id_token_string, google_requests.Request())      
      user = {        
            "username": idinfo.get("name"),
            "email": idinfo.get("email"),
            "avatar": idinfo.get("picture"),         
            "provider": "google",
            "provider_id": idinfo.get("sub"),
         }      
      # check email
      logging.warning('Google raw user: %s',user)
   
      user_db = db.query(User).filter(User.email == user['email']).first()
      logging.warning('DB user: %s',user_db)
            
      existing_user_email = str(user_db.email) if user_db else None
      
      if existing_user_email:
         logger.warning("Email already exists: %s", user['email'])
         # raise HTTPException(status_code=400, detail=["Email already existed. Login instead."]) 
         return user_db        
      
      logger.info("save_google_user_to_db: %s", user)
      google_user =User(**user)
      db.add(google_user)
      db.commit()
      db.refresh(google_user)      
      return google_user
      
   except HTTPException as http_ex:
      raise http_ex 
     
   except Exception as e:
      print("Unexpected error:", str(e))
      raise HTTPException(status_code=500, detail="Internal Server Error")