import logging
from fastapi import APIRouter
from core.config import settings
from urllib.parse import quote_plus,urlencode
from starlette.responses import RedirectResponse
from auth.app.services.google.helpers import save_google_user_to_db

logger = logging.getLogger("uvicorn.error") 

auth_google_router = APIRouter(prefix="/api/auth", tags=["google_auth"])

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_SCOPE = settings.GOOGLE_SCOPE
GOOGLE_RESPONSE_TYPE = settings.GOOGLE_RESPONSE_TYPE
GOOGLE_TOKEN_ENDPOINT = settings.GOOGLE_TOKEN_ENDPOINT
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
google_redirect_uri_fe = settings.GOOGLE_REDIRECT_URI_FE

# if settings.ENV.upper()=="DEV":  
#    google_redirect_uri_fe = google_redirect_uri_fe.split(",")[0]
# else:
#    # prod
#    google_redirect_uri_fe = settings.GOOGLE_REDIRECT_URI_FE

@auth_google_router.get("/google/login")
def google_login():
   params = {
      "client_id": GOOGLE_CLIENT_ID,
      "redirect_uri": GOOGLE_REDIRECT_URI,   
      "response_type": GOOGLE_RESPONSE_TYPE,
      "access_type": "offline",
      "prompt": "consent",
   }

   scope = quote_plus(GOOGLE_SCOPE, safe=" ")
   url = "https://accounts.google.com/o/oauth2/auth?" + urlencode(params) + f"&scope={scope}"
  
   logger.info("Redirecting to Google OAuth URL: %s", url)
   return RedirectResponse(url=url)


from fastapi import Request, Depends
from sqlalchemy.orm import Session
from core.session import get_db
import requests
from auth.app.schemas import RegisterFilter
from auth.app.services.custom import create_access_token

@auth_google_router.get("/google/callback")
def google_callback(request: Request,db: Session = Depends(get_db)):
   try:
      code = request.query_params.get("code")
      if not code:
         return {"error": "Auth code not found in request."}
      
      data = {
         "code": code,
         "client_id": GOOGLE_CLIENT_ID,
         "client_secret": GOOGLE_CLIENT_SECRET,
         "redirect_uri": GOOGLE_REDIRECT_URI,
         "grant_type": "authorization_code",
      }
      token_response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
      
      if token_response.status_code != 200:
         logger.error("Failed to exchange code for token: %s", token_response.text)      
         return {"error": "Failed to exchange code for token."}   
      
      token_data = token_response.json()
      id_token_str = token_data.get("id_token")

      g_user = save_google_user_to_db(id_token_str,db)
      # logger.info("TEST ONLY: Google User at google/callback: %s", g_user)
      g_access_token = token_data.get("access_token")  
      
      logger.info(f"TEST TEST g_access_token: {g_access_token}")
      
      user_obj = RegisterFilter.model_validate(g_user)
      user_dict = user_obj.model_dump()
      from fastapi.encoders import jsonable_encoder      
      user_dict = jsonable_encoder(user_dict)
      
      user_dict['message']="Google Login Success"     
      
      data = {
         "sub":user_dict['id'],
         "username":user_dict['username']
      }
      access_token = create_access_token(data)  
      
      response = RedirectResponse(url=google_redirect_uri_fe)   
      cookie_params = {
         "httponly": True,
         "samesite": "none",
         "secure": True,
         "max_age": 60*60*24*30
      }
      response.set_cookie(
         key="k8s_token",
         value=access_token,       
         **cookie_params
      )

      return response
   except Exception as e:
      import traceback
      from fastapi.responses import JSONResponse
      logger.error("Google callback failed: %s\n%s", e, traceback.format_exc())
      return JSONResponse({"detail": "EXCEPTION Internal Server Error"}, status_code=500)

