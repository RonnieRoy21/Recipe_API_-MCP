from enum import Enum
from typing import List
from pydantic import BaseModel, Field

# --- Enums for strict validation ---



# --- Nested Models ---

class Ingredient(BaseModel):
    id: int
    name: str
    category: str
    quantity: float
    unit: str
    optional: bool


class RecipeData(BaseModel):
    id: int
    name: str
    description: str
    difficulty: str
    meal_type: str
    cuisine: str
    dietary_tags: List[str]
    servings: int
    prep_time: int = Field(..., description="Preparation time in minutes")
    cook_time: int = Field(..., description="Cooking time in minutes")
    calories_per_serving: int
    protein: int
    instructions: List[str]
    ingredients: List[Ingredient]


class MetaData(BaseModel):
    language: str


# --- Main Root Model ---

class RecipeResponse(BaseModel):
    data: RecipeData
    meta: MetaData
