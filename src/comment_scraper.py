from urllib.request import urlopen
import json
import os
import re

TARGET_PATH_URLS = os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.json')
TARGET_PATH_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data', 'scraped_comments_raw.json')

TARGET_REGIONS = ['asia', 'africa', 'northamerica', 'southamerica', 'europe', 'oceania']

def build_url(recipe_id: str):
    url = f'https://api.chefkoch.de/v2/recipes/{recipe_id}/comments'
    return url

def get_json_from_url(url: str):
    response = urlopen(url)
    data = json.loads(response.read())
    return data

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def extract_comments_from_json(payload):
    comments = []

    for comment in payload['results']:
        text = comment['text']
        text_preprocessed = remove_emoji(text)
        text_preprocessed = text_preprocessed.replace('\r', '')
        text_preprocessed = text_preprocessed.replace('\n', '')
        comments.append(text_preprocessed)

    return comments

def import_target_urls(file_path):
        with open(file_path, 'r') as target_file:
            dataset = json.load(target_file)
        return dataset

def scrape_comments_by_recipes():
    target_urls = import_target_urls(TARGET_PATH_URLS)
    comments = dict()
    for region in target_urls['payload']:
        if region['region'] in TARGET_REGIONS:
            for url in region['urls']:
                print(f'[{region['urls'].index(url)}/{len(region['urls'])}] in {region["region"]}')
                recipe_id = url.split('/')[4]
                url = build_url(recipe_id)
                payload = get_json_from_url(url)
                comments[f'{recipe_id}'] = extract_comments_from_json(payload)
    return comments

if __name__ == '__main__':
    collected_comments = scrape_comments_by_recipes()
    payload_string = json.dumps(collected_comments, ensure_ascii=False, indent=2)

    with open(TARGET_PATH_EXPORT, 'w', encoding='utf-8') as file:
        file.write(payload_string)