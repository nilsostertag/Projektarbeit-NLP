import json
import data_structures as ds
from typing import List
import os

def import_recipe_from_json(file_path: str) -> ds.Recipes:
    if os.path.exists(file_path):
        with open(file_path, 'r') as source:
            source_data = json.load(source)
            imported_recipes = ds.Recipes

            for source_recipe in source_data['payload']:
                # retrieve recipe properties
                imported_nutritional_values = ds.Nutritional_Val(
                    kcal = source_recipe['properties']['nutritional_values']['kcal'],
                    protein = source_recipe['properties']['nutritional_values']['protein'],
                    fat = source_recipe['properties']['nutritional_values']['fat'],
                    carbs = source_recipe['properties']['nutritional_values']['carbs']
                )
                
                # retrieve nested dish time properties
                imported_dish_time = ds.Dish_Time(
                    prep = source_recipe['properties']['dish_time']['prep'],
                    cook = source_recipe['properties']['dish_time']['cook'],
                    sum_time = source_recipe['properties']['dish_time']['sum_time']
                )

                # retrieve ingredient list
                imported_ingredients = ds.Ingredients
                imported_ingredients.portions = source_recipe['ingrediants']['portions']
                for ingredient in source_recipe['ingredients']['payload']:
                    imported_ingredients.payload.append(ds.Ingredients(
                        name = ingredient['name'],
                        amount = ingredient['amount'],
                        unit = ingredient['unit']
                    ))

                imported_recipe = ds.Recipe(
                    region = source_recipe['region'],
                    recipe_id = source_recipe['recipe_id'],
                    url = source_recipe['link'],
                    title = source_recipe['title'],
                    author = source_recipe['author'],
                    properties = ds.Properties(
                        date_published = source_recipe['properties']['date_published'],
                        rating = source_recipe['properties']['rating'],
                        difficulty = source_recipe['properties']['difficulty'],
                        nutritional_values = imported_nutritional_values,
                        dish_time = imported_dish_time,
                        tags = source_recipe['properties']['tags']
                    ),
                    ingredients = imported_ingredients,
                    article = source_recipe['article']
                )
            
            imported_recipes.payload.append(imported_recipe)

        return imported_recipes
    else:
        return None