from datetime import datetime, timedelta, timezone
from core.config import settings
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request

from sqlalchemy.orm import Session
from core.session import get_db
from core.model import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta | None = None):
   to_encode = data.copy()
   current_utc_time = datetime.now(timezone.utc)
   
   if expires_delta:
      expire = current_utc_time + expires_delta
   else:
      expire = current_utc_time + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
   
   to_encode.update({
      "exp": expire.timestamp(),
      "iat": current_utc_time.timestamp(),
      "sub": str(data.get("sub")) if "sub" in data else None,
      "username": str(data.get("username")) if "username" in data else None,
   })
   
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   print(f"IMPORTANT encoded_jwt: {encoded_jwt}")
   return encoded_jwt

# data = {
#    "sub":"useriduseriduserid",
#    "username":"username"
# }

# create_access_token(data)
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

import re
email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
def validate_new_user(func):
   def wrapper(*args,**kwargs):
      username = kwargs.get("username") or (args[0] if len(args) > 0 else None)
      email = kwargs.get("email") or (args[1] if len(args) > 1 else None)
      password = kwargs.get("password") or (args[2] if len(args) > 2 else None)
      confirm_password = kwargs.get("confirm_password") or (args[3] if len(args) > 3 else None)

      # Validation
      if not username or len(username.strip()) < 6:
         raise HTTPException(status_code=400, detail="Username should have at least 6 characters!")
      if not email or not re.match(email_regex, email):
         raise HTTPException(status_code=400, detail="Email format is invalid!")
      if not password or len(password) < 8:
         raise HTTPException(status_code=400, detail="Password must have at least 8 characters!")
      if password != confirm_password:
         raise HTTPException(status_code=400, detail="Passwords do not match!")

      return func(*args, **kwargs) 
   return wrapper

@validate_new_user
def create_user(username,email, password, confirm_password):
   print(f"new user created with \nUsername: {username}\nEmail: {email}\nPassword length: {len(password)}")
   
# def validate_login(func):
#    def wrapper(email,password,*args,**kwargs):
#       if not re.match(email_regex,email):
#          raise ValueError("")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(pwd:str)->str:
   return pwd_context.hash(pwd)

def verify_password(plain_pwd:str, hashed_pwd:str)->bool:
   return pwd_context.verify(plain_pwd,hashed_pwd)
