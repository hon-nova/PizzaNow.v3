import logging
from fastapi import APIRouter,Request, Depends, HTTPException
from core import settings
import urllib.parse  
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests

from auth.app.schemas import RegisterFilter
from core.session import get_db
from auth.app.services.linkedin import save_linkedin_user_to_db
from auth.app.services.custom import create_access_token

auth_linkedin_router = APIRouter(prefix="/api/auth", tags=["linkedin_auth"])

logger = logging.getLogger("uvicorn.error") 
L_AUTHORIZATION_URL ="https://www.linkedin.com/oauth/v2/authorization"
# L_AUTHORIZATION_URL =settings.L_AUTHORIZATION_URL
L_TOKEN_URL=settings.L_TOKEN_URL
L_USER_URL=settings.L_USER_URL
L_CLIENT_ID=settings.L_CLIENT_ID
L_CLIENT_SECRET=settings.L_CLIENT_SECRET
L_SCOPE=settings.L_SCOPE
L_RESPONSE_TYPE=settings.L_RESPONSE_TYPE
L_STATE=settings.L_STATE
L_REDIRECT_URI=settings.L_REDIRECT_URI
l_redirect_url_fe=settings.L_REDIRECT_URI_FE


if settings.ENV.upper()=="DEV":  
   l_redirect_url_fe = l_redirect_url_fe.split(",")[0]
else:
   # prod
   l_redirect_url_fe = settings.L_REDIRECT_URI_FE

@auth_linkedin_router.get("/linkedin/login")
def linkedin_login():
   params = {
      "response_type": L_RESPONSE_TYPE,
      "client_id": L_CLIENT_ID,
      "redirect_uri": L_REDIRECT_URI,
      "scope": L_SCOPE,
      "state": L_STATE,
   }
   url = L_AUTHORIZATION_URL + "?" + urllib.parse.urlencode(params)
   logger.info("Redirecting to LinkedIn OAuth URL: %s", url)   
   return RedirectResponse(url=url)


@auth_linkedin_router.get("/linkedin/callback")
def linkedin_callback(request: Request, db: Session = Depends(get_db)):
   code = request.query_params.get("code")
   state = request.query_params.get("state")
   
   if not state or state != L_STATE:
      logger.error("State mismatch or state not provided.")
      return {"error": "State mismatch or state not provided."}   

   if not code:
      return {"error": "Authorization code not provided."}
   
   token_response  = requests.post(
      L_TOKEN_URL,
      data={
         "grant_type": "authorization_code",
         "code": code,        
         "redirect_uri": L_REDIRECT_URI,
         "client_id": L_CLIENT_ID,
         "client_secret": L_CLIENT_SECRET,
      },
   )
   if token_response.status_code != 200:
      raise HTTPException(status_code=token_response.status_code, detail=token_response.text)

   token_json = token_response.json()
   l_access_token = token_json.get("access_token")
   expires_in = token_json.get("expires_in")   
   
   profile_response = requests.get(
      L_USER_URL,
      headers={
         "Authorization": f"Bearer {l_access_token}",
         "X-Restli-Protocol-Version": "2.0.0"
      }
   )
   if profile_response.status_code != 200:
      raise HTTPException(status_code=profile_response.status_code, detail=profile_response.text)

   userinfo_data = profile_response.json()
   logger.info("LinkedIn user profile information retrieved: %s", userinfo_data)

   user = {        
         "username": userinfo_data.get("name"),
         "email": userinfo_data.get("email"),
         "avatar": userinfo_data.get("picture"),         
         "provider": "linkedin",
         "provider_id": userinfo_data.get("sub"),
      }      
   
   logging.warning('LinkedIn raw user: %s',user)
   l_user = save_linkedin_user_to_db(user,db)
   logging.warning('LinkedIn user SAVED: %s',l_user)      
   
   # user_dict = UserResponse.model_validate(user_db).model_dump()   
   user_obj = RegisterFilter.model_validate(l_user)
   user_dict = user_obj.model_dump()
   from fastapi.encoders import jsonable_encoder      
   user_dict = jsonable_encoder(user_dict)
   
   user_dict['message']="LinkedIn Login Success"  
   data = {
         "sub":user_dict['id'],
         "username":user_dict['username']
      }
   access_token = create_access_token(data)    
   response = RedirectResponse(url=l_redirect_url_fe)  
  
   # if settings.ENV.upper() == "DEV":         
   #    cookie_params = {
   #       "httponly": True,
   #       "samesite": "none",
   #       "secure": False,
   #       "max_age": 60*60*24*30 }
   # else:         
   #    cookie_params = {
   #       "httponly": True,
   #       "samesite": "none",
   #       "secure": True,
   #       "max_age": 60*60*24*30 }
      
   # response.set_cookie(
   #    key="k8s_token",
   #    value=access_token,
   #    domain=".pizzanow.local.com",
   #    **cookie_params
   # )   
   cookie_params = {
      "httponly": True,
      "samesite": "none",
      "secure": True,
      "max_age": 60*60*24*30
      }
   response.set_cookie(
      key="k8s_token",
      value=access_token,
      domain=".pizzanowai.studio",
      **cookie_params
   )
   return response
