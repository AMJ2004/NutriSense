from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,conlist
from typing import List,Optional
import pandas as pd
from model import recommend,output_recommended_recipes


dataset=pd.read_csv('/app/Data/dataset.csv',compression='gzip')

app = FastAPI(
    title="Nutrisense API",
    description="Diet Recommendation System API",
    version="1.0.0"
)

# Add CORS middleware for Streamlit Cloud compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class params(BaseModel):
    n_neighbors:int=5
    return_distance:bool=False

class PredictionIn(BaseModel):
    nutrition_input:conlist(float, min_items=9, max_items=9)
    ingredients:list[str]=[]
    params:Optional[params]


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


@app.get("/")
def home():
    return {"health_check": "OK"}


@app.post("/predict/",response_model=PredictionOut)
def update_item(prediction_input:PredictionIn):
    recommendation_dataframe=recommend(dataset,prediction_input.nutrition_input,prediction_input.ingredients,prediction_input.params.dict())
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

