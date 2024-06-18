import json
import data_structures as ds
from typing import List

def import_recipe_from_json(file_path: str) -> List[ds.Recipe]:
    with open(file_path, 'r') as source:
        source_data = json.load(source)
        imported_recipes = []

        for source_recipe in source_data:
            # retrieve recipe properties
            source['properties'] = source_recipe['properties']
            source['nutval'] = source['properties']['nutritional_values']

            imported_nutritional_values = ds.Nutritional_Val(
                kcal = source['nutval']['kcal'],
                protein = source['nutval']['protein'],
                fat = source['nutval']['fat'],
                carbs = source['nutval']['carbs']
            )
            
            # retrieve nested dish time properties
            source['dish_time'] = source['properties']['dish_time']
            imported_dish_time = ds.Dish_Time(
                prep = source['dish_time']['prep'],
                cook = source['dish_time']['cook'],
                sum_time = source['dish_time']['sum_time']
            )

            # retrieve ingredient list
            imported_ingredients = List[ds.Ingredient]
            for ingredient in source_recipe['ingredients']:
                imported_ingredients.append(ds.Ingredient(
                    name = ingredient['name'],
                    amount = ingredient['amount'],
                    unit = ingredient['unit']
                ))

            imported_recipe = ds.Recipe(
                id = source_recipe['id'],
                link = source_recipe['link'],
                title = source_recipe['title'],
                author = source_recipe['author'],
                properties = ds.Properties(
                    date_published = source['properties']['date_published'],
                    nutritional_val = imported_nutritional_values,
                    dish_time = imported_dish_time,
                    tags = source['properties']['tags']
                ),
                ingredients = imported_ingredients,
                article = source_recipe['article']
            )
        
        imported_recipes.append(imported_recipe)

    return imported_recipes