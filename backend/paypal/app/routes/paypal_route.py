import logging
import os

from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse

from core import settings
from paypal.app.schemas import OrderRequest

paypal_router = APIRouter(prefix="/api/paypal", tags=["paypal"])

PAYPAL_CLIENT_ID=settings. PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET=settings.PAYPAL_CLIENT_SECRET
PAYPAL_OAUTH2_TOKEN_URL=settings.PAYPAL_OAUTH2_TOKEN_URL
PAYPAL_CHECKOUT_ORDERS_URL=settings.PAYPAL_CHECKOUT_ORDERS_URL
PAYPAL_DOMAINS= settings.PAYPAL_DOMAINS

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
   except requests.RequestException as e:
      raise HTTPException(status_code=500, detail=str(e))
   #  "access_token": "A21AAIgqp5Bl4sx-HGYUS5CyIKotIEoN8pPjDQwVdmqurvTl2eBDDz41ryyfWmbbicdPdFj31DhUmfXpf50ZxYSzXlD0yNRoA"
   logging.info(f"resp.json() from PayPal: {resp.json()}")
   return resp.json()
   
from decimal import Decimal

# Create an order
@paypal_router.post("/orders")
def create_order(data: OrderRequest):
   token = get_access_token()
   # import uuid
   # paypal_request_id = str(uuid.uuid4())  
   # 44ae74c1-8499-4e32-86b2-21e7b8be3fe3
   payload = {
       "intent": "CAPTURE",
        "purchase_units": [
            {"amount": {"currency_code": "CAD", "value": Decimal(data.amount)}}
        ],
        "application_context": {
            "return_url": f"{PAYPAL_DOMAINS}/paypalReturnHome",
            "cancel_url": f"{PAYPAL_DOMAINS}/paypalCancel",
        },
   }
   # "A21AAIgqp5Bl4sx-HGYUS5CyIKotIEoN8pPjDQwVdmqurvTl2eBDDz41ryyfWmbbicdPdFj31DhUmfXpf50ZxYSzXlD0yNRoA",
   resp = requests.post(
      PAYPAL_CHECKOUT_ORDERS_URL,
      json=payload,
      headers={"Authorization": f"Bearer {token}"},
   )
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)
   logging.info(f"/orders resp.json(): {resp.json()}")
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
   return resp.json()

PAYPAL_BASE="https://api-m.sandbox.paypal.com"

@paypal_router.post("/orders/{order_id}/capture")
def capture_order(order_id:str):
   token = get_access_token()
   resp = requests.post(
      f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",    
      headers={"Authorization": f"Bearer {token}"},
      json={
         "payment_source": {
            "paypal": {
               "experience_context": {
                  "return_url": "https://pizzanow-v3.vercel.app/paypalReturnHome",
                  "cancel_url": "https://pizzanow-v3.vercel.app/paypalCancel",
               }
            }
         }
      }
   )
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)
   """
   keep: PayPal OrderId, status
   """
   logging.info(f"/{order_id}/capture resp.json(): {resp.json()}")
   return resp.json()

from paypal.app.schemas import OrderCreateRequest
from paypal.app.services import save_to_neon

@paypal_router.post("/orders/create")
def create_order_in_db(order: OrderCreateRequest):
  
   saved_order_id = save_to_neon(order)  # your DB function
   return {"order_id": saved_order_id, "status": "CREATED"}


from core.auth import get_current_user
from fastapi import Depends
from core.model import User
from core.schema import LoginFilter


@paypal_router.get("/auth",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   logging.info(f"paypal user in /auth route: {user.username}")
   base= LoginFilter.model_validate(user)
   # user_dict = base.model_dump()
   
   return base


