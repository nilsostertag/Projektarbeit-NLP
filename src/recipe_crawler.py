import os
import requests
from bs4 import BeautifulSoup

class recipe_crawler:

    def __init__(self, url_pre_page: str, page: int, url_past_page: str, max_pages: int):
        # build the specific page url
        # https://www.chefkoch.de/rs/s0t14/Asiatisch-Rezepte.html
        self.url_pre_page = url_pre_page
        self.page = page
        self.url_past_page = url_past_page
        self.search_base_url = self.build_base_url(self.url_pre_page, self.page, self.url_past_page)
        self.crawled_pages = []
        self.recipe_links = []
        self.max_pages = max_pages


    def collect_links(self, base_url) -> list:
        
        if base_url not in self.crawled_pages and self.page < self.max_pages:
            #print(f'Request {base_url} ...')
            self.base_html_content = requests.get(base_url).text

            # Retrieving recipe cards
            self.soup_base_html_content = BeautifulSoup(self.base_html_content, 'html.parser')
            self.recipe_cards = self.soup_base_html_content.find_all(class_='ds-recipe-card')

            # Collecting links from recipe cards
            for card in self.recipe_cards:
                link = card.find('a')['href']
                self.recipe_links.append(link)
                print(f'URLs collected:    {len(self.recipe_links)}')

            self.crawled_pages.append(base_url)

            self.page += 1
            self.search_base_url = self.build_base_url(self.url_pre_page, self.page, self.url_past_page)

            return self.collect_links(self.search_base_url)

        else:
            return self.recipe_links

    def build_base_url(self, url_pre_page: str, page: int, url_past_page: str) -> str:
        search_base_url = f'{url_pre_page}s{page}{url_past_page}'
        return search_base_url

    def save_target_urls(self, to_save: list):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'target_urls.txt')
        try:
            with open(file_path, 'w') as file_target_URLs:
                for url in to_save:
                    file_target_URLs.write(url + '\n')
            print('Target URLs have been saved.')
        except:
            print('Error while saving target URLs.')


if __name__ == '__main__':
    rc = recipe_crawler('https://www.chefkoch.de/rs/', 0, 't14/Asiatisch-Rezepte.html', max_pages=1)
    recipe_links = rc.collect_links(rc.search_base_url)
    
    for link in recipe_links:
        print(link)
    print(f'{len(recipe_links)} Links have been collected.')

    rc.save_target_urls(recipe_links)