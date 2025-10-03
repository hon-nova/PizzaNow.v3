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
   
   capture_id = payload["resource"]["id"]         # 42311647XV020574X
   order_id = payload["resource"]["supplementary_data"]["related_ids"]["order_id"]
   status = payload["resource"]["status"]

    # Match against *paypal_order_id* you stored earlier (order_id, not capture_id!)
   order = db.query(Order).filter(Order.paypal_order_id == order_id).first()

   if order:
      order.payment_status = status
      db.commit()
      return {"message": "ok"}
   else:
      print("No matching order found for", order_id)
      return {"message": "order not found"}
   
   # event_type = payload.get("event_type")
   # resource = payload.get("resource", {})
   # paypal_order_id = resource.get("id")

   # if not paypal_order_id:
   #    raise HTTPException(status_code=400, detail="Missing order ID")

   # # Find order by PayPal order ID
   # order = db.query(Order).filter(Order.paypal_order_id == paypal_order_id).first()
   # if not order:
   #    raise HTTPException(status_code=404, detail="Order not found")

   # if event_type == "PAYMENT.CAPTURE.COMPLETED":
   #    print(f"@webhooks/paypal/capture: current event_type: {event_type}")
   #    order.payment_status = "COMPLETED"
   # elif event_type == "PAYMENT.CAPTURE.DENIED":
   #    print(f"@webhooks/paypal/capture: current event_type: {event_type}")
   #    order.payment_status = "DENIED"
   # else:
   #    # Ignore other events
   #    print(f"@webhooks/paypal/capture: current event_type: {event_type}")
   #    return {"status": "ignored"}

   # db.commit()
   # return {"status": order.payment_status, "order_id": order.id}
