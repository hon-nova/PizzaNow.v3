from pydantic_settings import BaseSettings
import os
from pathlib import Path

ENV = os.getenv("ENV", "DEV").upper() 
env_file = ".env" if ENV == "DEV" else ".env.prod"

class Settings(BaseSettings):  
   
   ENV: str = ENV
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
   PAYPAL_OAUTH2_TOKEN_URL: str=""
   PAYPAL_CHECKOUT_ORDERS_URL: str=""  
   
   
   class Config:          
      env_file = Path(__file__).parent / ".env"      
      extra = "forbid" 

settings = Settings() # pyright: ignore[reportCallIssue]
