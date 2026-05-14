from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
import pandas as pd
import os
from model import recommend,output_recommended_recipes

# Global dataset variable
dataset = None

app = FastAPI(title="NutriSense API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input: Annotated[list[float], Field(min_length=9, max_length=9)]
    ingredients: list[str] = []
    params: Optional[params] = None


class Recipe(BaseModel):
    Name:str
    CookTime:str
    PrepTime:str
    TotalTime:str
    RecipeIngredientParts:list[str]
    Calories:float
    FatContent:float
    SaturatedFatContent:float
    CholesterolContent:float
    SodiumContent:float
    CarbohydrateContent:float
    FiberContent:float
    SugarContent:float
    ProteinContent:float
    RecipeInstructions:list[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None


@app.on_event("startup")
async def startup_event():
    global dataset
    try:
        data_path = '/app/Data/dataset.csv'
        if os.path.exists(data_path):
            dataset = pd.read_csv(data_path, compression='gzip')
            print(f"Dataset loaded successfully: {dataset.shape}")
        else:
            print(f"Warning: Dataset not found at {data_path}")
    except Exception as e:
        print(f"Error loading dataset: {e}")


@app.get("/")
def home():
    return {"health_check": "OK", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "dataset_loaded": dataset is not None}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    if dataset is None:
        return {"output": None}
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

