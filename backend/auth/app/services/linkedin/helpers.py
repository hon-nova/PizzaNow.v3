from sqlalchemy.orm import Session
from core.model import User
import logging
from fastapi import HTTPException, Depends
logger = logging.getLogger("uvicorn.error")
from core.session import get_db

def save_linkedin_user_to_db(raw_user:dict, db: Session = Depends(get_db)):
   try:
      user_db = db.query(User).filter(User.email == raw_user['email']).first()
      
      existing_user_email = str(user_db.email) if user_db else None
      
      if existing_user_email:
         
         return user_db
   
      linked_user =User(**raw_user)
      db.add(linked_user)
      db.commit()
      db.refresh(linked_user) 
           
      return linked_user
   except Exception as e:
     
      raise HTTPException(status_code=500, detail="Failed to save LinkedIn user to db")