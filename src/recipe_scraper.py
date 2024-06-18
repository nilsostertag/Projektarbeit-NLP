import os
import requests
import utils.data_structures as ds
import utils.data_export as de
from bs4 import BeautifulSoup
from typing import List
from re import sub
from datetime import datetime
from math import nan

TARGET_PATH_SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.txt')

TARGET_PATH_URLS = os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.txt')
TARGET_PATH_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data', 'scraped_recipes.json')

class Recipe_Scraper:
    def __init__(self, target_url_file):
        self.target_URLs = self.import_target_urls(file_path = target_url_file)
        self.buffered_HTMLs: List[ds.Recipe_HTML_preprocessed] = []
        self.scraped_recipes: ds.Recipes = ds.Recipes(payload = [])
    
    def buffer_recipe(self, request_url):
        request_buffer = requests.get(request_url).text

        temp_buffer_soup = BeautifulSoup(request_buffer, 'html.parser')

        temp_buffer_articles = temp_buffer_soup.find_all('article')

        # find preparation field because of attribute error
        temp_buffer_prep = None
        for element in temp_buffer_articles:
            attributes = ''.join(element.attrs['class'])
            if not 'recipe' in attributes:
                temp_buffer_prep = element

        temp_buffer = ds.Recipe_HTML_preprocessed(
            url = request_url,
            header = temp_buffer_soup.find('article', class_ = 'recipe-header'),
            ingredients = temp_buffer_soup.find('article', class_ = 'recipe-ingredients'),
            nutrition = temp_buffer_soup.find('article', class_ = 'recipe-nutrition'),
            preparation = temp_buffer_prep,
            tags = temp_buffer_soup.find('div', class_ = 'recipe-tags'),
            author = temp_buffer_soup.find('div', class_ = 'recipe-author')
        )
        
        return temp_buffer

    def scrape_data_raw(self, buffer: ds.Recipe_HTML_preprocessed) -> ds.Recipe:
        scr_url = str(buffer.url)
        scr_id = scr_url.split('/')[4]

        #TODO: strip date and difficulty from unnecessary signs
        if buffer.author != None:
            scr_author = buffer.author.find('span')
            if scr_author != None:
                scr_author = scr_author.text
                scr_author = self.process_author(scraped_author = scr_author)

        if buffer.header != None:
            scr_title = buffer.header.find('h1').text
            scr_rating = buffer.header.find('div', class_ = 'ds-rating-avg').find('strong').text
            scr_publishdate = buffer.header.find('span', class_ = 'recipe-date').text.strip()
            if scr_publishdate != None:
                scr_publishdate = self.process_publishdate(scraped_publishdate = scr_publishdate)

            scr_difficulty = buffer.header.find('span', class_ = 'recipe-difficulty').text.strip()
            if scr_difficulty != None:
                scr_difficulty = self.process_difficulty(scraped_difficulty = scr_difficulty)

        elif buffer.header == None:
            scr_title, scr_author, scr_publishdate, scr_difficulty = None
            scr_rating = nan
                
        if buffer.nutrition != None:
            scr_nut = buffer.nutrition.find_all('div', class_ = 'ds-col-3')
            if scr_nut != None:
                scr_nut = self.process_nutrition(scraped_nut = scr_nut)
        elif buffer.nutrition == None:
            scr_nut = None
        
        if buffer.preparation != None:
            scr_dt = buffer.preparation.find_all('span', class_ = 'rds-recipe-meta__badge')
            if scr_dt != None:
                scr_dt = self.process_dish_time(scraped_dish_time = scr_dt)
            
            scr_preparation = buffer.preparation.find_all('div', class_ = 'ds-box')
            if scr_preparation != None:
                scr_preparation = self.process_preparation(scraped_preparation = scr_preparation)

        elif buffer.preparation == None:
            scr_dt, scr_preparation = None

        if buffer.tags != None:
            scr_tags = buffer.tags.find_all('a', class_ = 'ds-tag bi-tags')
            if scr_tags != None:
                scr_tags = self.process_tags(scraped_tags = scr_tags)

        elif buffer.tags == None:
            scr_tags = None

        if buffer.ingredients != None:
            scr_ingredients_portions = buffer.ingredients.find('input', class_ = 'ds-input').get('value')
            scr_ingredients = buffer.ingredients.find_all('table', 'ingredients table-header')
            if scr_ingredients != None:
                scr_ingredients = self.process_ingredients(scraped_ingredients = scr_ingredients, scraped_portions = scr_ingredients_portions)
        
        elif buffer.scr_ingredients == None:
            scr_ingredients = None


        scraped_content = ds.Recipe(
            recipe_id = scr_id,
            url = scr_url,
            title = scr_title,
            author = scr_author,
            properties = ds.Properties(
                date_published = scr_publishdate,
                rating = float(scr_rating),
                difficulty = scr_difficulty,
                nutritional_values = scr_nut,
                dish_time = scr_dt,
                tags = scr_tags
            ),
            ingredients = scr_ingredients,
            preparation = scr_preparation
        )

        return scraped_content

    def process_author(self, scraped_author) -> str:
        result = scraped_author.split(' ')[len(scraped_author.split(' ')) - 1]
        
        return result

    def process_publishdate(self, scraped_publishdate) -> str:
        val = sub(r'[^\w\s]', '', scraped_publishdate).strip()

        date_format = '%d%m%Y'

        dt = datetime.strptime(val, date_format)
    
    # Convert the datetime object to a Unix timestamp
        timestamp = int(dt.timestamp())
        return timestamp

        return val

    def process_difficulty(self, scraped_difficulty) -> str:
        val = sub(r'[^\w\s]', '', scraped_difficulty).strip()
        return val

    def process_nutrition(self, scraped_nut) -> ds.Nutritional_values:
        result = ds.Nutritional_values(None, None, None, None)
        for element in scraped_nut:
            tag = str(element.find('h5').text).lower()
            val = element.text.split('\n')[len(element.text.split('\n'))-2].strip()

            match tag:
                case 'kcal':
                    result.kcal = int(val)
                case 'eiweiß':
                    result.protein = val
                case 'fett':
                    result.fat = val
                case 'kohlenhydr.':
                    result.carbs = val
                case _0:
                    pass

        return result

    def process_dish_time(self, scraped_dish_time) -> ds.Dish_time:
        result = ds.Dish_time(None, None, None)
        for element in scraped_dish_time:
            tag = element.text.split('\n')[len(element.text.split('\n'))-2].strip().lower()
            val = sub(r'\D', '', tag)

            if 'arbeit' in tag:
                result.prep = int(val)
            elif 'koch' in tag:
                result.cook = int(val)
            elif 'gesamt' in tag and result.prep != None and result.cook != None:
                result.sum_time = int(result.prep) + int(result.cook)
            elif 'geasmt' in tag:
                result.sum_time = int(val)

        return result

    def process_tags(self, scraped_tags) -> List[str]:
        result = []
        
        for element in scraped_tags:
            val = str(element.text.strip().lower())
            result.append(val)

        return result

    def process_ingredients(self, scraped_ingredients, scraped_portions) -> ds.Ingredients:
        result = ds.Ingredients(portions = None, payload = None)
        result_payload = []

        for ingredient_list in scraped_ingredients:
            buffered_ingredients = ingredient_list.find_all('tr')
            for element in buffered_ingredients:
                if element.find('td', class_ = 'td-left') != None:
                    amount = ''
                    unit = ''
                    amount_unit = element.find('td', class_ = 'td-left').text.strip().lower().split(' ')
                    if amount_unit != None:
                        for e in amount_unit:
                            if e.isdigit():
                                amount = e
                            elif not e.isdigit() and e != '':
                                unit = e
                        ingredient = element.find('td', class_ = 'td-right').text.strip().lower()
                        buffer_result = ds.Ingredient_payload(
                            name = ingredient,
                            amount = amount,
                            unit = unit
                        )
                        result_payload.append(buffer_result)

        result.portions = int(scraped_portions)
        result.payload = result_payload
        return result

    def process_preparation(self, scraped_preparation) -> str:
        buffer_strings = []

        for element in scraped_preparation:
            buffer_str = element.text
            buffer_strings.append(buffer_str)

        buffer_prep = max(buffer_strings, key = len)
        result = buffer_prep.replace('\n', '')

        return result.lower()

    def import_target_urls(self, file_path):
        target_urls = []
        with open(file_path, 'r') as target_file:
            for target_url in target_file:
                target_urls.append(target_url)

        return target_urls
    
    def execute_process(self):
        for target in self.target_URLs:
            print(f'[{self.target_URLs.index(target)}/{len(self.target_URLs)}] Buffering {target}')
            temp_buffer = self.buffer_recipe(target)
            print(f'[{self.target_URLs.index(target)}/{len(self.target_URLs)}] Processing {target}')
            temp_data = self.scrape_data_raw(temp_buffer)
            self.scraped_recipes.payload.append(temp_data)
            #self.buffered_HTMLs.append(temp_buffer)

        """
            for buffered_HTML in self.buffered_HTMLs:
            print(f'[{self.buffered_HTMLs.index(buffered_HTML)}/{len(self.buffered_HTMLs)}] Processing {buffered_HTML.url}')
            temp_data = self.scrape_data_raw(buffered_HTML)
            self.scraped_recipes.payload.append(temp_data)
        """
        payload_string = self.scraped_recipes.to_json()
        #print(payload_string)
        de.export_to_json_v2(str(payload_string), TARGET_PATH_EXPORT)

        

if __name__ == '__main__':
    rs = Recipe_Scraper(target_url_file = TARGET_PATH_URLS)
    rs.execute_process()