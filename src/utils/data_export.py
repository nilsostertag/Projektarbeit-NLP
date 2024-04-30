import json
import data_structures as ds

class RecipeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ds.Recipe):
            return {
                "link": obj.link,
                "recipe_id": obj.recipe_id,
                "title": obj.title,
                "author": obj.author,
                "properties": {
                    "date_published": obj.properties.date_published,
                    "nutritional_val": {
                        "kcal": obj.properties.nutritional_val.kcal,
                        "protein": obj.properties.nutritional_val.protein,
                        "fat": obj.properties.nutritional_val.fat,
                        "carbs": obj.properties.nutritional_val.carbs
                    },
                    "dish_time": {
                        "prep": obj.properties.dish_time.prep,
                        "cook": obj.properties.dish_time.cook,
                        "sum_time": obj.properties.dish_time.sum_time
                    },
                    "tags": obj.properties.tags
                },
                "ingredients": [
                    {"name": ing.name, "amount": ing.amount, "unit": ing.unit} for ing in obj.ingredients
                ],
                "article": obj.article
            }

def export_to_json(obj, path, encoder):
    with open(path, 'w+') as file:
        json.dump(obj, file, cls = encoder, indent = 4)