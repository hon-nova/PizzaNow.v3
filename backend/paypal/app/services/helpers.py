from paypal.app.schemas import OrderCreateRequest
from paypal.app.models import Order
from sqlalchemy.orm import Session

def save_to_neon(order: OrderCreateRequest,db: Session):
   new_order_item = Order(
      user_id = order.user_id,
      cart_items = order.cart_items,
      discount = order.discount,
      shipping_fee = order.shipping_fee,
      taxes = order.taxes,
      total = order.total )
   
   db.add(new_order_item)
   db.commit()
   print(f"@save_to_neon new order_id: {new_order_item.id} added to Order Neon.")
   return new_order_item.id