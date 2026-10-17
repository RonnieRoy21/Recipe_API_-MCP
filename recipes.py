from pydantic import ValidationError
import requests,os
from requests.exceptions import RequestException
from dotenv import load_dotenv
from models.recipe import RecipeData,Ingredient,RecipeResponse
from typing import List
# Method	Endpoint	Description
# GET	/recipes	List recipes with filters
# GET	/recipes/random	Get a random recipe
# GET	/recipes/{id}	Get recipe details
# GET	/ingredients	List ingredients
# GET	/ingredients/{id}	Get ingredient details

class Recipes():
    def __init__(self):
        load_dotenv()
        self.recipe_url="https://recipeapi.io/api/v1/"
        self.api_key:str=os.getenv("recipe_api_key")

        self.headers={
            "Authorization":f"Bearer {self.api_key}"
        }
        if self.api_key:
            print("Api key is read correctly")
        else:
            print("No api key read")


#________________FORMAT THE RECIPE INGREDIENTS_________________________
    def format_ingredients(self,ingreds:List[Ingredient]):
        """
        Args:
            ingreds (List[Ingredient]): _description_
        """
        if not ingreds:
            print("No ingredients Listed")
            return     
        print(f"____________Ingredients____________\n")
        for i in ingreds:
            print(f"Name: {i.name}")
            print(f"Quantity: {i.quantity}")
            print(f"Category: {i.category}")
            print(f"Unit(of measure): {i.unit}\n")
        print("_______________END OF INGRREDIENTS_____________\n")
        return

    

#______________FORMAT THE RECIPE INSTRUCTIONS(COMMAND LINE USE)____________________
    def format_instructions(self,instr:List[str]):
        if not instr:
            print("No Instructions found")
            return
        print("___________How To Cook It__________\n")
        for i,step in enumerate(instr):
            print(f"{i}. {step}\n")

        print("___________ ENJOY ___________\n")



#__________________FETCH A RANDOM RECIPE _____________________
    def get_random_recipe(self):
        """
        Raises:
            ve: _description_
            re: _description_

        Returns:
            _type_: _description_
        """
        try:
            random_recipes=requests.get(url=f"{self.recipe_url}/recipes/random",headers=self.headers)
            if random_recipes.status_code == 200:
                api_data=random_recipes.json()
                recipe_data=api_data['data']
                recipe=RecipeData.model_validate(recipe_data)
                print(f"Name: {recipe.name}")
                print(f"Description: {recipe.description}")
                self.format_ingredients(ingreds=recipe.ingredients)
                self.format_instructions(instr=recipe.instructions)
                return {
                    'name':recipe.name,
                    'description':recipe.description,
                    'ingredients': recipe.ingredients,
                    'instructions':recipe.instructions
                }
        except ValidationError as ve:
            print(f"Validation Error: {ve.errors()}")
            raise ve
        except requests.exceptions.RequestException as re:
            print(f"Error occured: {re.strerror}")
            print(random_recipes.status_code)
            raise re

        
##____________________GET A LIST OF RECIPES__________________

    def get_recipes(self):
     
        try:
            response=requests.get(url=f"{self.recipe_url}/recipes",headers=self.headers)
            if response.status_code == 200:
                recipe_json=response.json()
                data=recipe_json["data"]
                print(f"Data parsed {data}")
                recipes=[RecipeData.model_validate(d) for d in data]
                return recipes
            print("fetch failed")
            return []
        except RequestException as re:
            print(f"Error fetching recipes.{re.strerror}")
            raise re
        except Exception as e:
            print(f"Other Error: {e.args}")
            raise e


#________________________GET SPECIFIC RECIPE BY ITS ID_______________________
    def get_recipe_by_id(self,r_id:int):
    
        try:
            if not r_id:
                raise "Id Must be Provided"
            response=requests.get(f"{self.recipe_url}/recipes/{r_id}",headers=self.headers)
            print(f"Response code {response.status_code}")
            if response.status_code == 200:
                data=response.json()
                recipe_details=data["data"]
                recipe=RecipeData.model_validate(recipe_details)
                return recipe
            return "No recipe found"
        except RequestException as re:
            print(f"Error getting recipe no. {r_id}.{re.strerror}")
            raise re
        except ValidationError as ve:
            print(f"Validation error: {ve.errors()}")
            raise "Validation Error"


#_______________________GET A LIST OF RECIPES BY INGREDIENTS_______________________
    def get_recipe_by_ingredients(self,ingridients:List[str]):
        try:
            if not ingridients:
                raise "Missing parameters (ingredients)"
            single_string=""
            for i in ingridients:
                single_string+=f"{str(i)},"
            param={"ingridients":f"{single_string}"}
            response=requests.get(url=f"{self.recipe_url}/recipes",headers=self.headers,params=param)

            match(response.status_code):
                case 200:
                    data=response.json()
                    recipe_details=data["data"]
                    recipes=[RecipeData.model_validate(d) for d in recipe_details]
                    return recipes
                case 404:
                    raise "Ingredients not found"
                case 429:
                    raise "Can't Process.Too many requests"
        except RequestException as re:
            print(f"Error fetching ingredients.{re.strerror}")
            raise re
        except Exception as e:
            raise e

        
            



#_______________________GET A LIST OF INGREDIENTS___________________________

    def get_ingredients(self):
        try:
            response=requests.get(url=f"{self.recipe_url}/ingredients",headers=self.headers)
            if response.status_code == 200:
                data=response.json()
                ingrids=data["data"]
                return {
                    "Total Ingrids":len(ingrids),
                    "Ingredients":ingrids
                }
        except RequestException as re:
            raise re
        except Exception as e:
            raise e


        
if __name__=="__main__":
    recipes=Recipes()

    recipes.get_random_recipe()
