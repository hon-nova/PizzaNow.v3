from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import settings

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
   
   return encoded_jwt
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
   
   
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pwd: str) -> str:
    """
    Hash a password safely with bcrypt.
    - Ensures it's a string
    - Strips whitespace
    - Truncates to 72 bytes (bcrypt limit)
    """
    if not isinstance(pwd, str):
        raise ValueError(f"Password must be a string, got {type(pwd)}")

    # normalize & truncate
    pwd = pwd.strip()
    pwd_bytes = pwd.encode("utf-8")
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        pwd = pwd_bytes.decode("utf-8", errors="ignore")

    return pwd_context.hash(pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    """
    Verify a password safely.
    - Returns False if inputs are invalid
    - Handles bcrypt's 72-byte limit
    """
    if not plain_pwd or not hashed_pwd:
        return False
    if not isinstance(plain_pwd, str) or not isinstance(hashed_pwd, str):
        return False

    plain_pwd = plain_pwd.strip()
    plain_bytes = plain_pwd.encode("utf-8")
    if len(plain_bytes) > 72:
        plain_bytes = plain_bytes[:72]
        plain_pwd = plain_bytes.decode("utf-8", errors="ignore")

    try:
        return pwd_context.verify(plain_pwd, hashed_pwd)
    except Exception:
        return False

