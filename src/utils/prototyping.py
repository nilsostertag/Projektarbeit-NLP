import json
import os

JSON_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw_data', 'scraped_recipes.json')

def import_test(file):
    f = open(file, encoding='utf8')
    data = json.load(f)
    print(len(data['payload']))
    
    return data

if __name__ == '__main__':
    import_test(JSON_PATH)
