from fastapi import APIRouter
from google.auth import default
from app.core.config import settings

test_router = APIRouter()
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

@test_router.get("/ping")
def ping():
   return {"message": "pong"}

@test_router.get("/test-cors")
async def test_cors():
   return {"allowed_origins": origins}

@test_router.get("/whoami")
async def whoami():
   from google.oauth2.service_account import Credentials as SA_Credentials
   try:
      creds, project_id = default()
      if isinstance(creds, SA_Credentials):
         email = creds.service_account_email
      else:
         # fallback for ADC types like Cloud Run
         email = getattr(creds, "_service_account_email", None) or "⚠️ Not a service account"
      return {
         "project_id": project_id,
         "service_account_email": email
      }
   except Exception as e:
      return {
         "project_id": None,
         "service_account_email": None,
         "error": str(e)
      }

