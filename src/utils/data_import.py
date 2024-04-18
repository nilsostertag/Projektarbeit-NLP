import json
import data_structures as ds
from typing import List

def import_recipe_from_json(file_path: str) -> List[ds.Recipe]:
    with open(file_path, 'r') as source:
        source_data = json.load(source)
        imported_recipes = []

        for source_recipe in source_data:
            # retrieve nested object properties
            source_properties = source_recipe['properties']
            source_nutval = source_properties['nutritional_values']
            source_dish_time = source_properties['dish_time']

            imported_nutritional_values = ds.Nutritional_Val(
                kcal = source_nutval['kcal'],
                protein = source_nutval['protein'],
                fat = source_nutval['fat'],
                carbs = source_nutval['carbs']
            )

            imported_dish_time = ds.Dish_Time(
                prep = source_dish_time['prep'],
                cook = source_dish_time['cook'],
                sum_time = source_dish_time['sum_time']
            )

            imported_recipe = ds.Recipe(
                id = source_recipe['id'],
                link = source_recipe['link'],
                title = source_recipe['title'],
                author = source_recipe['author'],
                properties = ds.Properties(
                    date_published = source_properties['date_published'],
                    nutritional_val = imported_nutritional_values,
                    dish_time = imported_dish_time,
                    tags = source_properties['tags']
                ),
                ingredients = source_recipe['ingredients'],
                article = source_recipe['article']
            )
        
        imported_recipes.append(imported_recipe)

    return imported_recipes