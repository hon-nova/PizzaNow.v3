import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision import models
from PIL import Image
import pandas as pd

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Step 1: Prepare ingredient classes ---
df = pd.read_csv("awsscripts/pizza_ingredients.csv")
# Extract unique ingredients
ingredients_set = set()
for ings in df['ingredients']:
    ingredients_set.update([i.strip() for i in ings.split('|') if i])
    
ingredient_classes = sorted(list(ingredients_set))
num_classes = len(ingredient_classes)
ingredient_to_idx = {ing: idx for idx, ing in enumerate(ingredient_classes)}
idx_to_ingredient = {idx: ing for ing, idx in ingredient_to_idx.items()}


# --- Step 2: Define a simple model ---
class PizzaModel(nn.Module):
   def __init__(self, num_classes):
      super().__init__()
      # pretrained CNN backbone
      self.backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
      self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)
      
   def forward(self, x):
      return self.backbone(x)

# --- Step 3: Load model ---
BEST_MODEL_PATH = "awsscripts/models/pizza_ingredients_best.pt"

def load_model(num_classes):
   model = PizzaModel(num_classes)
   state = torch.load(BEST_MODEL_PATH, map_location=device)
   # check if it's state_dict
   if not isinstance(state, dict):
      model = state
      assert isinstance(model, PizzaModel)
   model.to(device)
   model.eval()
   return model

model = load_model(num_classes)

# --- Step 4: Prediction ---
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
])

from torch import Tensor
import requests
from io import BytesIO
def predict_ingredients(url: str, threshold: float = 0.5) -> list[str]:   
   
   try:
      response = requests.get(url, timeout=5)  # 5 seconds max
      response.raise_for_status()
      img = Image.open(BytesIO(response.content)).convert("RGB")
   except Exception as e:
      print(f"Skipping {url}, download/open failed: {e}")
      return []   
   
   x_tensor: Tensor = transform(img)     # type: ignore
   x_batch: Tensor = x_tensor.unsqueeze(0).to(device)    

   with torch.no_grad():
      outputs: Tensor = torch.sigmoid(model(x_batch)).squeeze(0)
      
   preds = (outputs > threshold).nonzero(as_tuple=True)[0].tolist()
   return [idx_to_ingredient[i] for i in preds]
 
 
# url = "https://pizzanowimages.s3.us-east-1.amazonaws.com/000001.jpg"
# ingredients = predict_ingredients(url)
# print(ingredients)