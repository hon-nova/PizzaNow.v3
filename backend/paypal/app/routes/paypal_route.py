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

param = {
   "paypal_client_id":PAYPAL_CLIENT_ID,
   "paypal_client_secret":PAYPAL_CLIENT_SECRET,
   "grant_type":"client_credentials"
}
# @paypal_router.post("??")
# def get_access_token():
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

   return resp.json()

   
from decimal import Decimal
# Create an order
@paypal_router.post("/orders")
def create_order(data: OrderRequest):
   token = get_access_token()
   payload = {
       "intent": "CAPTURE",
        "purchase_units": [
            {"amount": {"currency_code": "CAD", "value": Decimal(data.amount)}}
        ],
        "application_context": {
            "return_url": "https://pizza-now-ai.vercel.app/paypalReturnHome",
            "cancel_url": "https://pizza-now-ai.vercel.app/paypalCancel",
        },
   }
   resp = requests.post(
      PAYPAL_CHECKOUT_ORDERS_URL,
      json=payload,
      headers={"Authorization": f"Bearer {token}"},
   )
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)
   return resp.json()

PAYPAL_BASE="https://api-m.sandbox.paypal.com"

@paypal_router.post("/orders/{order_id}/capture")
def capture_order(order_id:str):
   token = get_access_token()
   resp = requests.post(
      f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",    
      headers={"Authorization": f"Bearer {token}"},
   )
   if resp.status_code >= 300:
      raise HTTPException(resp.status_code, resp.text)
   return resp.json()



# PayPal client setup
# paypal_client: PaypalServersdkClient = PaypalServersdkClient(
#     client_credentials_auth_credentials=ClientCredentialsAuthCredentials(
#         o_auth_client_id=settings.PAYPAL_CLIENT_ID,
#         o_auth_client_secret=settings.PAYPAL_CLIENT_SECRET,
#     ),
#     logging_configuration=LoggingConfiguration(
#         log_level=logging.INFO,
#         mask_sensitive_headers=False,
#         request_logging_config=RequestLoggingConfiguration(
#             log_headers=True, log_body=True
#         ),
#         response_logging_config=ResponseLoggingConfiguration(
#             log_headers=True, log_body=True
#         ),
#     ),
# )

# orders_controller: OrdersController = paypal_client.orders

# # Health check
# @paypal_router.get("/")
# def index():
#    return {"message": "Server is running"}

# # Create an order
# @paypal_router.post("/orders")
# def create_order(payload: dict):
#     try:
#         cart = payload.get("cart", [])
#         # Currently hard-coded to 100 USD; you can compute from cart
#         order = orders_controller.create_order(
#             {
#                 "body": OrderRequest(
#                     intent=CheckoutPaymentIntent.CAPTURE,
#                     purchase_units=[
#                         PurchaseUnitRequest(
#                             AmountWithBreakdown(currency_code="USD", value="100.00")
#                         )
#                     ],
#                 ),
#                 "prefer": "return=representation",
#             }
#         )
#         return JSONResponse(content=ApiHelper.json_serialize(order.body))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Capture an order
# @paypal_router.post("/orders/{order_id}/capture")
# def capture_order(order_id: str):
#     try:
#         order = orders_controller.capture_order(
#             {"id": order_id, "prefer": "return=representation"}
#         )
#         return JSONResponse(content=ApiHelper.json_serialize(order.body))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
"""
{
    "scope": "https://uri.paypal.com/services/payments/futurepayments https://uri.paypal.com/services/invoicing https://uri.paypal.com/services/vault/payment-tokens/read https://uri.paypal.com/services/disputes/read-buyer https://uri.paypal.com/services/payments/realtimepayment https://uri.paypal.com/services/disputes/update-seller https://uri.paypal.com/services/payments/payment/authcapture openid https://uri.paypal.com/services/disputes/read-seller Braintree:Vault https://uri.paypal.com/services/payments/refund https://api.paypal.com/v1/vault/credit-card https://api.paypal.com/v1/payments/.* https://uri.paypal.com/payments/payouts https://uri.paypal.com/services/vault/payment-tokens/readwrite https://api.paypal.com/v1/vault/credit-card/.* https://uri.paypal.com/services/subscriptions https://uri.paypal.com/services/applications/webhooks",
    "access_token": "A21AAIaDtnKgTfqzCdfXMRCHS-U-p2mKQXnH-AQub9ZmRLu7x_fpG__W2HBU-9zS796lSzNKMrEStdhjbfMHo9Qn8qcmzgypg",
    "token_type": "Bearer",
    "app_id": "APP-80W284485P519543T",
    "expires_in": 32400,
    "nonce": "2025-09-10T20:57:40ZE0RBfp-JI3M9l9lUcgiFUwfzbJ0As2I2Q1DwvR_Ttgw"
}
"""


