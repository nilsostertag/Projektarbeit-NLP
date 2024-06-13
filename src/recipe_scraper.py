import os
import requests
import utils.data_structures as ds
#import utils.data_export as de
from bs4 import BeautifulSoup
from typing import List

TARGET_PATH_SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.txt')

TARGET_PATH_URLS = os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.txt')
TARGET_PATH_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data', 'scraped_recipes.json')

class Recipe_Scraper:
    def __init__(self, target_url_file):
        self.target_URLs = self.import_target_urls(file_path = target_url_file)
        self.buffered_HTMLs: List[ds.Recipe_HTML_preprocessed] = []
        self.scraped_recipes: List[ds.Recipe] = []
    
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

        processed_recipe = ds.Recipe(None, None, None, None, None, None, None)

        scr_url = str(buffer.url)
        scr_id = scr_url.split('/')[4]
        scr_title = buffer.header.find('h1').text
        scr_author = buffer.author.find('span').text

        scr_publishdate = buffer.header.find('span', class_ = 'recipe-date').text
        scr_difficulty = buffer.header.find('span', class_ = 'recipe-difficulty').text

        scr_nut = buffer.nutrition.find_all('div', class_ = 'ds-col-3')
        scr_nut = self.process_nutrition(scraped_nut = scr_nut)
        

        '''scraped_data = ds.Recipe(
            id = scraped_id,
            link = scraped_url,
            title = scraped_title,
            author = scraped_author,
            properties = scraped_properties,
            ingredients = scraped_ingredients,
            article = scraped_article
        )'''

    def process_nutrition(self, scraped_nut) -> ds.Nutritional_Val:
        result = ds.Nutritional_Val(None, None, None, None)
        for element in scraped_nut:
            tag = str(element.find('h5').text).lower()
            val = element.text.split('\n')[len(element.text.split('\n'))-2].strip()


            match tag:
                case 'kcal':
                    result.kcal = val
                case 'eiweiß':
                    result.protein = val
                case 'fett':
                    result.fat = val
                case 'kohlenhydr.':
                    result.carbs = val
                case _0:
                    pass

        return result

    def process_dish_time(self, scraped_dish_time) -> ds.Dish_Time:
        #TODO
        pass

    def process_tags(self, scraped_tags):
        #TODO
        pass

    def process_ingredients(self, scraped_ingredients):
        #TODO
        pass

    def process_preparation(self, scraped_preparation) -> str:
        #TODO
        pass

    def import_target_urls(self, file_path):
        target_urls = []
        with open(file_path, 'r') as target_file:
            for target_url in target_file:
                target_urls.append(target_url)

        return target_urls
    
    def execute_process(self):
        for target in self.target_URLs:
            temp_buffer = self.buffer_recipe(target)
            self.buffered_HTMLs.append(temp_buffer)

        for buffered_recipe in self.buffered_HTMLs:
            temp_data = self.scrape_data_raw(buffered_recipe)
            self.scraped_recipes.append(temp_data)

        

if __name__ == '__main__':
    rs = Recipe_Scraper(target_url_file = TARGET_PATH_SAMPLE)
    rs.execute_process()