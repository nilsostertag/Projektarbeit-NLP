import os
import requests
import utils.data_structures as ds
import utils.data_export as de
from bs4 import BeautifulSoup
from typing import List

TARGET_PATH_SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.txt')

TARGET_PATH_URLS = os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.txt')
TARGET_PATH_EXPORT = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data', 'scraped_recipes.json')
MAX_BUFFER_SIZE = 48

class Recipe_Scraper:
    def __init__(self, target_url_file):
        self.target_URLs = self.import_target_urls(file_path = target_url_file)
        self.buffered_HTMLs: List[ds.Recipe_HTML_preprocessed] = []
        self.scraped_recipes: List[ds.Recipe] = []
    
    def buffer_recipe(self, request_url):
        request_buffer = requests.get(request_url).text

        temp_buffer_soup = BeautifulSoup(request_buffer, 'html.parser')
        temp_buffer = ds.Recipe_HTML_preprocessed(
            url = request_url,
            header = temp_buffer_soup.find('article', class_ = 'recipe-header'),
            ingredients = temp_buffer_soup.find('article', class_ = 'recipe-ingredients'),
            nutrition = temp_buffer_soup.find('article', class_ = 'recipe-nutrition'),
            preparation = temp_buffer_soup.find('article', class_ = {'ds-box' 'ds-grid-float' 'ds-col-12' 'ds-col-m-8' 'ds-or-3'})
        )
        
        return temp_buffer

    def scrape_data_raw(self, buffer: ds.Recipe_HTML_preprocessed) -> ds.Recipe:
        print(f'TYPE: {type(buffer.header)}')
        scraped_url = str(buffer.url)
        print(scraped_url)
        scraped_id = scraped_url.split('/')[4]
        print(scraped_id)
        scraped_title = buffer.header.find('h2').text
        print(scraped_title)
        scraped_author = buffer.preparation.find('a', attrs={'data-vars-bi-username'}).text
        print(scraped_author)
        '''scraped_data = ds.Recipe(
            id = scraped_id,
            link = scraped_url,
            title = scraped_title,
            author = scraped_author,
            properties = scraped_properties,
            ingredients = scraped_ingredients,
            article = scraped_article
        )'''

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