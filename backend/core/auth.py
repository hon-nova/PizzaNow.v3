from core.session import get_db
from core.model import User
from core.config import settings

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError

def decode_token(token: str):
   try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
      sub: str | None = payload.get("sub")
      username: str | None = payload.get("username")

      if not isinstance(sub,str):
         raise HTTPException(status_code=401, detail="Invalid token: no subject")

      return {"sub": sub, "username": username}

   except JWTError:
      raise HTTPException(status_code=401, detail="Invalid or expired token") 
   
def get_current_user(request: Request,db: Session = Depends(get_db)):
   token = request.cookies.get("access_token")
   if not token:
      raise HTTPException(status_code=401, detail="Not authenticated")

   user_data = decode_token(token)
   user = db.query(User).filter(
         (User.username == user_data['username']) | (User.id == user_data['sub'])
      ).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
   
   return user  
 