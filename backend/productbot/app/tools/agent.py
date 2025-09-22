from typing import TypedDict

class AppState(TypedDict):
   home: str
   login: str
   cart: str
   payment: str

def read_products():
   pass
def home():
   products: list[dict]
   
   def get_products():
      products = read_products()
      return products
   
   return [get_products]

def login():
   pass
   
def run_app(state: AppState):
   if state.get("home")=="home":
      return "home"
   elif state.get("login")=="login":
      return "login"   
   elif state.get("cart")=="cart":
      return "cart"
   elif state.get("payment")=="payment":
      return "payment"