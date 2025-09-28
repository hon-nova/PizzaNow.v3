from app.core import SessionLocal
from sqlalchemy.orm import Session
from app.models import Pizza

def get_all_pizzas(db: Session = SessionLocal() ,page=1, limit=8):
   try:
      offset = (page - 1) * limit

      pizzas_query = db.query(Pizza).offset(offset).limit(limit)
      total_count = db.query(Pizza).count()
      pizzas = pizzas_query.all()

      array_return = []
      for pizza in pizzas:
         array_return.append({
            "id": str(pizza.id),
            "name": pizza.name,
            "description": pizza.description,
            "full_price": str(pizza.full_price),
            "slice_price": str(pizza.slice_price),
            "image_url": pizza.image_url,
            "ingredients": pizza.ingredient_list,
            "type":pizza.type
         })

      return {
         "pizzas": array_return,
         "total": total_count,
         "page": page,
         "limit": limit,
         "pages": (total_count + limit - 1)
      }

   except Exception as e:
      db.rollback()
      raise e