from typing import List
from fastmcp import FastMCP
from fastapi import FastAPI,HTTPException,status
from recipes import Recipes
from mcp_model import mcp_app

app=FastAPI(title="Roxy Recipe APP",lifespan=mcp_app.lifespan)


recipe=Recipes()

#get random recipe
@app.get("/random-recipe")
def get_random_recipe():
    try:
        return recipe.get_random_recipe()
    except Exception as e:
        raise HTTPException(detail=e.args,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#get all recipes
@app.get("/recipes")
def get_recipes():
    try:
       return  recipe.get_recipes()
    except Exception as e:
        raise HTTPException(detail=e.args,status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
#get recipes by name or id
@app.post("/recipe/{recipeId}")
def get_recipe(recipeId:int):
    try:
        return recipe.get_recipe_by_id(r_id=recipeId)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.args
        )

#get recipe by ingredients
@app.post("/recipe-by-ingredients")
def get_recipe_by_Ingredients(ingredients:List[str]):
    try:
        if not ingredients:
            raise HTTPException(detail="Missing Parameters",status_code=status.HTTP_400_BAD_REQUEST)
        return recipe.get_recipe_by_ingredients(ingridients=ingredients)
    except Exception as e:
        raise HTTPException(
            detail=e.args,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


#get a list of available ingredients
@app.get("/get-ingredients")
def get_list_of_ingredients():
    try:
        return recipe.get_ingredients()
    except Exception as e:
        raise HTTPException(
            detail=e.args,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


app.mount(path="/agent-roxy",app=mcp_app)

