from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

SECRET_FILE = Path("/etc/config/.env.secret")
LOCAL_ENV_FILE = Path(__file__).parent / ".env"

if SECRET_FILE.exists():
    load_dotenv(dotenv_path=SECRET_FILE, override=True)

else:
   load_dotenv(dotenv_path=LOCAL_ENV_FILE, override=True)

class Settings(BaseSettings):  
   
   ENV: str = "DEV"
   VERTEX_REGION: str = "us-central1"  
   PROJECT_ID: str = "dummy-project"
   ALLOWED_ORIGINS: str = "*"
   DATABASE_URL: str = ""
   SECRET_KEY: str = "secret"
   ALGORITHM: str = ""
   ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
   
   GOOGLE_CLIENT_ID: str =""
   GOOGLE_CLIENT_SECRET: str="" 
   GOOGLE_SCOPE: str = ""
   GOOGLE_RESPONSE_TYPE: str =""
   GOOGLE_TOKEN_ENDPOINT: str= ""
   GOOGLE_REDIRECT_URI: str =""   
   GOOGLE_REDIRECT_URI_FE: str=""
   # L_AUTHORIZATION_URL: str=""
   L_TOKEN_URL: str=""
   L_USER_URL: str=""
   L_CLIENT_ID: str=""
   L_CLIENT_SECRET: str=""
   L_SCOPE: str=""
   L_RESPONSE_TYPE:str=""
   L_STATE:str=""
   L_REDIRECT_URI:str=""
   L_REDIRECT_URI_FE: str = ""
   # FE_PORT: str=""
   AWS_ACCESS_KEY_ID: str =""
   AWS_SECRET_ACCESS_KEY: str =""
   AWS_REGION: str =""
   AWS_S3_BUCKET: str=""
   
   PAYPAL_CLIENT_ID: str=""
   PAYPAL_CLIENT_SECRET: str=""
   PAYPAL_DOMAINS: str=""
   PAYPAL_OAUTH2_TOKEN_URL: str=""
   PAYPAL_CHECKOUT_ORDERS_URL: str=""  
   PAYPAL_DOMAINS_BE: str=""
   PAYPAL_DOMAINS_FE: str=""   
   
   class Config:     
      extra = "ignore"   

settings = Settings() # pyright: ignore[reportCallIssue]
print("@core/config: test os.getenv DATABASE_URL")
print(os.getenv("DATABASE_URL")) 


# settings.load_secrets()
   # def load_secrets(self):
   #    if SECRET_DIR.exists():
   #       for f in SECRET_DIR.iterdir():
   #          if f.is_file():
   #             # If file is a key=value env file
   #             for line in f.read_text().splitlines():
   #                if "=" in line:
   #                   k, v = line.split("=", 1)
   #                   os.environ[k] = v.strip()
