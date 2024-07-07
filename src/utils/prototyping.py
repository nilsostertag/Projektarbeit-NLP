import json
import os
import data_handling as dh
import data_import as di

JSON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw_data', 'scraped_recipes_raw.json')


if __name__ == '__main__':
    data = di.import_recipe_from_json(JSON_PATH)
    
    rand = dh.randomizer()
    var = rand.get_random_recipe(data.payload, False)
    print(var)
