
from decimal import Decimal
# from core.session import SessionLocal
from core.model import Pizza
from core.config import settings

import torch
from PIL import Image
import requests
from io import BytesIO
from joblib import load

from pathlib import Path
from uuid import uuid4
import boto3
from torchvision import transforms, models
from torchvision.models import ResNet18_Weights
import joblib
# CONFIG: pizza names
image_names =[
   "Three Cheese Bacon Wonder",
   "Four Cheese Inferno",
   "Five Cheese Overkill",
   "Cheddar Jack Storm",
   "Blue Cheese Crumble",
   "Gorgonzola Fantasy",
   "Parmesan Firestorm",
   "Cheese Lava Burst",
   "Feta Dreamscape",
   "Mozzarella Melt",
   "Creamy Ricotta Pizza",
   "Smoked Gouda Gold",
   "Brie Luxe",
   "Asiago Heaven",
   "Swiss Cheese Slide",
   "Cheese Trance",
   "Triple Layer Cheese",
   "Sharp White Cheese Heat",
   "Bocconcini Basil Pie",
   "Cheese-Stuffed Crust",
   "Pepperoni Blaze",
   "Sausage Supreme",
   "Meat Lover’s Madness",
   "BBQ Beef Fire",
   "Bacon Melt",
   "Spicy Beef Inferno",
   "Canadian Classic",
   "Ham Delight",
   "Spicy Italian",
   "Tandoori Sausage Crunch",
   "Chicken Mushroom Rage",
   "Ranch Chicballen Delight",
   "Prosciutto Luxury",
   "Double Bacon Feast",
   "Beefy Volcano",
   "Smoky BBQ Pepperoni",
   "Tex-Mex Beef",
   "Korean Bulgogi Pizza",
   "Pulled Pork Sizzle",
   "Margherita Supreme",
   "Garden Fresh",
   "Spicy Veggie Tango",
   "Four Cheese Burst",
   "Basil & Tomato",
   "Greek Veggie",
   "Maple Bacon Glory",
   "Roasted Veggie Medley",
   "Mushroom Overload",
   "Spinach Feta Classic",
   "Corn Fiesta",
   "Veggie Delight",
   "Jalapeño Crunch",
   "Truffle Mushroom Bliss",
   "Zucchini & Tomato",
   "Olive Dream",
   "Herbivore Special",
   "Veggie Pesto Charm",
   "Broccoli White Pie",
   "Garlic Garden Fling",
   "Eggplant Roast Pie",
   "Creamy Alfredo Veg",
   "Avocado Lime Pie",
   "Bell Pepper Riot",
   "Paneer Tikka Pizza",
   "Sweet Potato Veggie",
   "Beetroot Goat Cheese Avocado",
   "Sun-Dried Tomato Swirl",
   "Caprese Pizza",
   "Kimchi Veg Blaze",
   "Bruschetta Flat",
   "Ghost Pepper Heat",
   "Sweet Habanero Punch",
   "Firecracker Pie",
   "Szechuan Thunder",
   "Dragon Breath Pizza",
   "Sweet Chili Lime Explosion",
   "Spicy Tikka Inferno",
   "Peri Peri Scream",
   "Korean Green Garden",
   "Wasabi Cheese Dream",
   "Hot & Sweet Jalapeño",
   "Spicy Chorizo Blast",
   "Hatch Green Chili Pie",
   "Vindaloo Flame Pizza",
   "Cayenne Pepper Storm",
   "Hot Honey Pepperoni",
   "Sriracha Veg Surprise",
   "Scorpion Sauce Slice",
   "Spicy Pineapple Kick",
   "Red Pepper Cream Heat",
   "Tabasco Fire Pie",
   "Buffalo Inferno Deluxe",
   "Volcanic BBQ Burn",
   "Blazing Garlic Sauce",
   "Sweet 'n Spicy Mix",
   "Chimichurri Blaze",
   "Spicy Gochujang Pie",
   "Calabrian Chili Crunch",
   "Zesty Pepper Cream",
   "Inferno Margherita",
   "Green Garden Delight",
   "Spinach Pesto Crunch",
   "Zucchini Zen",
   "Broccoli & Cheddar Melt",
   "Mushroom Medley",
   "Vegan Supreme",
   "Roasted Veggie Riot",
   "Peppers & Onions Inferno",
   "Tomato Basil Bliss",
   "Philly Cheesesteak Pizza",
   "Olive Orchard Special",
   "Carrot Topper",
   "Sun-Dried Tomato Tango",
   "Corn & Black Bean Fiesta",
   "Artichoke Amore",
   "Herbivore’s Heaven",
   "Veggie Volcano",
   "Crispy Duck Hoisin",
   "Mutton Masala",
   "Crispy Hoisin",
   "Sweet Chili Green"
]

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY
AWS_REGION=settings.AWS_REGION
AWS_S3_BUCKET=settings.AWS_S3_BUCKET

# boto3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# def upload_local_pizzas_to_s3(local_folder: str = LOCAL_FOLDER) -> list[str]:
#    """Upload local images to S3 and return presigned URLs."""
#    urls = []
#    folder_path = Path(local_folder)
#    if not folder_path.exists() or not folder_path.is_dir():
#       raise FileNotFoundError(f"{local_folder} not found")

#    for file_path in folder_path.iterdir():
#       if not file_path.is_file() or file_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
#          continue

#       key = f"{S3_FOLDER}/{uuid4()}_{file_path.name}"
#       s3_client.upload_file(
#          str(file_path),
#          AWS_S3_BUCKET,
#          key
#       )

#       # Generate presigned URL valid for 1 hour
#       url = s3_client.generate_presigned_url(
#          "get_object",
#          Params={"Bucket": AWS_S3_BUCKET, "Key": key},
#          ExpiresIn=3600
#       )
#       urls.append(url)
#       print(f"Uploaded {file_path.name} → presigned URL")

#    return urls

def generate_description(name: str) -> str:
   return f"Delicious {name}. Perfectly baked and loved by all."

def generate_price_tiers():
   from random import randint
   full_price = Decimal(randint(23, 44))
   slice_price = round(full_price / 6, 2)
   return full_price, slice_price

def get_all_s3_image_urls() -> list[str]:
   """Return a list of public URLs for all images in the bucket folder"""
   urls = []
   paginator = s3_client.get_paginator("list_objects_v2")
   for page in paginator.paginate(Bucket=AWS_S3_BUCKET):     
      for obj in page.get("Contents", []):
         key = obj["Key"]
         if not key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
         url = f"https://{AWS_S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
         # https://pizzanowimages.s3.us-east-1.amazonaws.com/000001.jpg
        
         urls.append(url)
         
   return urls

from core.session import SessionLocal
# """alias pyawsscripts="/Users/honnguyen/Desktop/aws/venv/pizzanow/awsscripts/bin/python"
# pyawsscripts -m awsscripts.util
# """
from awsscripts import predict_ingredients
def seed_pizzas():
   session = SessionLocal()
   try:
      image_urls = get_all_s3_image_urls()  # now returns presigned URLs

      for url, name in zip(image_urls, image_names):
         full_price, slice_price = generate_price_tiers()

         # If an image fails to open, skip it safely
         try:
            ingredients = predict_ingredients(url)
            pizza = Pizza(
               name=name,
               description=generate_description(name),
               full_price=full_price,
               slice_price=slice_price,
               image_url=url,
               ingredients=ingredients,
               pizza_type="null"         
               )
            session.add(pizza)
            
         except Exception as e:
            print(f"ingredients {url}, e: {e}")           

      session.commit()
      print(f"Seeded {len(image_urls)} pizzas to Neon.")

   except Exception as e:
      session.rollback()
      print(f"Error during seeding: {e}")

   finally:
      session.close()

seed_pizzas()
