import json
import utils.data_structures as ds

def export_to_json(string: str, path: str):
    with open(path, 'w', encoding='utf8') as file:
        file.write(string)