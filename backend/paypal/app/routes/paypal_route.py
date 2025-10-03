import logging
import uuid
from fastapi import APIRouter,HTTPException
from datetime import datetime
import json
from core import settings
from paypal.app.schemas import OrderRequest,OrderCreateRequest, OrderOut
from paypal.app.services import save_to_neon
from core.auth import get_current_user
from core.model import User
from core.schema import LoginFilter

from core.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Body


paypal_router = APIRouter(prefix="/api/paypal", tags=["paypal"])

PAYPAL_BASE="https://api-m.sandbox.paypal.com"
PAYPAL_CLIENT_ID=settings.PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET=settings.PAYPAL_CLIENT_SECRET
PAYPAL_OAUTH2_TOKEN_URL=settings.PAYPAL_OAUTH2_TOKEN_URL
PAYPAL_CHECKOUT_ORDERS_URL=settings.PAYPAL_CHECKOUT_ORDERS_URL
PAYPAL_DOMAINS_BE= settings.PAYPAL_DOMAINS_BE
PAYPAL_DOMAINS_FE= settings.PAYPAL_DOMAINS_FE

param = {
   "paypal_client_id":PAYPAL_CLIENT_ID,
   "paypal_client_secret":PAYPAL_CLIENT_SECRET,
   "grant_type":"client_credentials"
}

import requests
def get_access_token():
   try:
      resp = requests.post(
         PAYPAL_OAUTH2_TOKEN_URL,
         data={"grant_type": "client_credentials"},
         auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
         headers={"Accept": "application/json"}
      )
      resp.raise_for_status()     
      return resp.json()['access_token']
   except requests.RequestException as e:
      raise HTTPException(status_code=500, detail=str(e))    

from decimal import Decimal, ROUND_HALF_UP
@paypal_router.post("/orders")
def create_order(data: OrderRequest):
   token = get_access_token()
   print("IMPORTANT: access_token: {token}")
   try:
      Decimal(str(data.amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
   except Exception as e:
      raise HTTPException(status_code=400, detail=f"Invalid amount: {data.amount}")
   amount = str(data.amount)  
   payload = {
      "intent": "CAPTURE",
      "purchase_units": [
         {"amount": {"currency_code": "CAD", "value": str(amount)}}
      ],
      "application_context": {
         
         "return_url": PAYPAL_DOMAINS_FE,
         "cancel_url":PAYPAL_DOMAINS_FE,
      },
   }
   resp = requests.post(
      PAYPAL_CHECKOUT_ORDERS_URL,
      json=payload,
      headers={
         "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"},
   )
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)
  
   created_order_return = resp.json()  
   order_id = created_order_return["id"]
   created_order_return["application_context"] = {
         
         "return_url": PAYPAL_DOMAINS_FE + "/products?success={order_id}",
         "cancel_url":PAYPAL_DOMAINS_FE + "/user/cart?error=cancelled",
      },
   
   return order_id

@paypal_router.post("/orders/{order_id}/capture")
def capture_and_save(order_id:str,payload:dict = Body(...),db:Session=Depends(get_db)):     
   token = get_access_token()
   logging.info(f"order_id: {order_id}")
   
   status = capture_status(order_id,token) 

   # 3. Build OrderCreateRequest manually
   order_data = {
      "user_id": payload["user_id"],
      "paypal_order_id": order_id,
      "payment_status":payload.get("payment_status","PENDING"),
      "discount": payload.get("discount", 0),
      "shipping_fee": payload.get("shipping_fee", 0),
      "taxes": payload.get("taxes", 0),
      "total": payload.get("total", 0),
      "items": payload["cart_items"],  # MUST exist        
   }
   
   order_req = OrderCreateRequest(**order_data)  
   order_req.payment_status = status  
   save_to_neon(order_req,db)  
   
   return status  
      
   # return  RedirectResponse(url=f"{PAYPAL_DOMAINS_BE}/api/paypal/success")   


def capture_status(order_id:str,token:str):       
   resp = requests.post(
      f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",    
      headers={
         "Content-Type":"application/json",
         "Authorization": f"Bearer {token}",
         "PayPal-Request-Id": str(uuid.uuid4())}, 
      
      json={}     
      )   
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)

   paypal_resp = resp.json() 
   
   return paypal_resp["status"]
   
from fastapi.responses import RedirectResponse

from core.session import SessionLocal
from core.model import Order

@paypal_router.get("/success")
def payment_success(order_id: str = None,db: Session = Depends(get_db)):   
   token = get_access_token()
   print(f"token @success: {order_id}")
   if not order_id:
      return {"error": "No PayPal order id provided"}
   
   # Capture the payment
   saved_order = db.query(Order).filter(Order.paypal_order_id == order_id).first()
   status = capture_status(saved_order.paypal_order_id,token) 
   
   # PAYPAL confirms the order's payment_status
   saved_order.payment_status = status
   db.commit()
   print(f"TEST captured_order_id: {saved_order.id}, status: {status}")
   
   return RedirectResponse(url=f"{PAYPAL_DOMAINS_FE}/products?success={status}")  
            

# @paypal_router.get("/cancel")
# def paypal_cancel():
#    """Handle failed/canceled payment from PayPal."""
  
#    return RedirectResponse(url=f"{PAYPAL_DOMAINS_FE}/user/cart?error=Transaction%20Cancelled%21")


@paypal_router.get("/auth",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   logging.info(f"paypal user in /auth route: {user.username}")
   base= LoginFilter.model_validate(user)
   # user_dict = base.model_dump()
   
   return base

"""{
    "id": "7W328831TJ718173M",
    "status": "CREATED",
    "links": [
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/7W328831TJ718173M",
            "rel": "self",
            "method": "GET"
        },
        {
            "href": "https://www.sandbox.paypal.com/checkoutnow?token=7W328831TJ718173M",
            "rel": "approve",
            "method": "GET"
        },
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/7W328831TJ718173M",
            "rel": "update",
            "method": "PATCH"
        },
        {
            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/7W328831TJ718173M/capture",
            "rel": "capture",
            "method": "POST"
        }
    ]
}"""

"""
logging.info(f"TEST ONLY @paypal_router")    

saved = db.query(Order).filter(Order.paypal_order_id == order_id).first()  
order_out = OrderOut.from_orm(saved)      

logging.info(json.dumps(order_out.model_dump(), default=str,indent=2))
# OR logging.info(order_out.model_dump_json(indent=2))
   logging.info(f" DURING STATUS COMPLETED ...")      """     


