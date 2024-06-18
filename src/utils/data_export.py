import json
import utils.data_structures as ds

def export_to_json(obj, path):
    with open(path, 'w') as file:
        json.dump(obj, file, indent = 2)

def export_to_json_v2(string: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(string)