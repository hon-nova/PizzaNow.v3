from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from core.session import get_db
from core.model import Order
import logging

webhook_router = APIRouter(prefix="/webhooks/paypal")

@webhook_router.post("/capture")
async def handle_paypal_capture(request: Request, db: Session = Depends(get_db)):
   """
   Handle PayPal capture events:
   - COMPLETED -> mark order completed
   - DENIED -> mark order denied
   """
   payload = await request.json()
   print("WEBHOOK PAYLOAD:", payload)
   
   capture_id = payload["resource"]["id"]        
   order_id = payload["resource"]["supplementary_data"]["related_ids"]["order_id"]
   status = payload["resource"]["status"]

   order = db.query(Order).filter(Order.paypal_order_id == order_id).first()

   if order:
      order.payment_status = status
      db.commit()
      return {"message": "ok"}
   else:
      print("No matching order found for", order_id)
      return {"message": "order not found"}
   
   