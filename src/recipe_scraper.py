import os
import requests
import utils.data_structures as ds
from bs4 import BeautifulSoup

MAX_BUFFER_SIZE = 48

class Recipe_Scraper:
    def __init__(self, target_url_file):
        self.target_URLs = self.read_target_urls(target_url_file)
        self.buffered_HTML = []
    
    def scrape_recipe(self, url) -> ds.Recipe:
        pass

    def read_target_urls(self, file_path):
        target_urls = []
        with open(file_path, 'r') as target_file:
            for target_url in target_file:
                target_urls.append(target_url)

        return target_urls

if __name__ == '__main__':
    rs = Recipe_Scraper(os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.txt'))