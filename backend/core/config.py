from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

def load_environment():
  
   SECRET_FILE = Path("/etc/secret-pizzanow/.env.secret")
   CONFIG_FILE = Path("/etc/config-pizzanow/.env.config")
   LOCAL_ENV_FILE = Path(__file__).parent / ".env"

   
   for env_file in [SECRET_FILE, CONFIG_FILE, LOCAL_ENV_FILE]:
      if env_file.exists():
         load_dotenv(dotenv_path=env_file, override=True)
         env_vars = dotenv_values(dotenv_path=env_file)
         os.environ.update(env_vars)
         print(f"@core/load_environment: loaded {env_file}")
      else:
         print(f"@core/load_environment: skipped {env_file} (not found)")

   print("@core/load_environment: DATABASE_URL =", os.getenv("DATABASE_URL"))


load_environment()

class Settings(BaseSettings):  
   
   ENV: str ="" 
   VERTEX_REGION: str =""
   PROJECT_ID: str ="" 
   ALLOWED_ORIGINS: str =""
   DATABASE_URL: str =""
   SECRET_KEY: str ="" 
   ALGORITHM: str =""
   ACCESS_TOKEN_EXPIRE_MINUTES: int=30 
   
   GOOGLE_CLIENT_ID: str =""
   GOOGLE_CLIENT_SECRET: str =""
   GOOGLE_SCOPE: str =""
   GOOGLE_RESPONSE_TYPE: str ="" 
   GOOGLE_TOKEN_ENDPOINT: str =""
   GOOGLE_REDIRECT_URI: str =""  
   GOOGLE_REDIRECT_URI_FE: str =""
   
   L_TOKEN_URL: str =""
   L_USER_URL: str =""
   L_CLIENT_ID: str =""
   L_CLIENT_SECRET: str =""
   L_SCOPE: str =""
   L_RESPONSE_TYPE:str =""
   L_STATE:str =""
   L_REDIRECT_URI:str =""
   L_REDIRECT_URI_FE: str =""
   
   AWS_ACCESS_KEY_ID: str =""
   AWS_SECRET_ACCESS_KEY: str ="" 
   AWS_REGION: str ="" 
   AWS_S3_BUCKET: str =""
   
   PAYPAL_CLIENT_ID: str =""
   PAYPAL_CLIENT_SECRET: str =""
   PAYPAL_DOMAINS: str =""
   PAYPAL_OAUTH2_TOKEN_URL: str =""
   PAYPAL_CHECKOUT_ORDERS_URL: str =""  
   PAYPAL_DOMAINS_BE: str =""
   PAYPAL_DOMAINS_FE: str =""
   
   class Config:     
      extra = "ignore"   

settings = Settings() # pyright: ignore[reportCallIssue]


