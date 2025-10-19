from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID as UUIDType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from core.model import Order, OrderItem
from paypal.app.schemas import OrderCreateRequest, OrderOut

def order_to_dict(order):
    return {
        "id": str(order.id),
        "user_id": str(order.user_id),
        "paypal_order_id": order.paypal_order_id,
        "discount": float(order.discount),
        "shipping_fee": float(order.shipping_fee),
        "taxes": float(order.taxes),
        "total": float(order.total),
        "transaction_date": order.transaction_date.isoformat(),
        "shipment_status": order.shipment_status,
    }
def _quantize_money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def save_to_neon(order: OrderCreateRequest, db: Session) -> Order:
    
   if order.paypal_order_id:
      existing = db.query(Order).filter(Order.paypal_order_id == order.paypal_order_id).first()
      if existing:
         return existing
   try:      
      new_order = Order(
         user_id=UUIDType(order.user_id),
         paypal_order_id=order.paypal_order_id,   
         payment_status = order.payment_status,             
         discount=_quantize_money(order.discount),
         shipping_fee=_quantize_money(order.shipping_fee),
         taxes=_quantize_money(order.taxes),
         total=_quantize_money(order.total),
      )

      db.add(new_order)
      db.flush()      
      
      for item in order.items:
         oi = OrderItem(
            order_id=new_order.id,
            pizza_id=UUIDType(item.pizza_id),
            quantity=int(item.quantity),
            sub_amount=_quantize_money(item.sub_amount),
         )
         db.add(oi)           
         
      db.commit()
      db.refresh(new_order)  
    
      return new_order

   except SQLAlchemyError:     
      db.rollback()
      raise
