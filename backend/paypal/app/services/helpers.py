from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID as UUIDType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from paypal.app.models import Order, OrderItem
from paypal.app.schemas import OrderCreateRequest

def _quantize_money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def save_to_neon(order: OrderCreateRequest, db: Session) -> Order:
   """
   Persist an Order + its OrderItems. Idempotent by paypal_order_id.
   - `order` is a Pydantic OrderCreateRequest (must include paypal_order_id set)
   - returns the created (or existing) Order ORM object
   """
    # idempotency: avoid duplicate DB rows if capture retried
   if order.paypal_order_id:
      existing = db.query(Order).filter(Order.paypal_order_id == order.paypal_order_id).first()
      if existing:
         return existing

   try:
        # transaction scope: either everything saves or nothing     
      new_order = Order(
         user_id=UUIDType(order.user_id),
         paypal_order_id=order.paypal_order_id,
         discount=_quantize_money(order.discount),
         shipping_fee=_quantize_money(order.shipping_fee),
         taxes=_quantize_money(order.taxes),
         total=_quantize_money(order.total),
         # shipment_status defaults to "pending" in model if configured
      )
      """new_order = Order(
        user_id=order.get("user_id"),
        paypal_order_id=order.get("paypal_order_id"),
        cart_items=order.get("cart_items"),
        discount=order.get("discount", 0),
        shipping_fee=order.get("shipping_fee", 0),
        taxes=order.get("taxes", 0),
        total=order.get("total"),
        shipment_status="pending"
    )"""
      db.add(new_order)
      db.flush()  # ensures new_order.id populated

      # create line items
      for item in order.cart_items:
         oi = OrderItem(
            order_id=new_order.id,
            pizza_id=UUIDType(item.pizza_id),
            quantity=int(item.quantity),
            sub_amount=_quantize_money(item.sub_amount),
         )
         db.add(oi)

      db.flush()
      db.refresh(new_order)  # load relationships if needed

      return new_order

   except SQLAlchemyError:
      # the context manager rolls back automatically, but be explicit for clarity
      db.rollback()
      raise
