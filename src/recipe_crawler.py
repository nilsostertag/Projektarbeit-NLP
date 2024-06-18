"""
Autor:     Ostertag

Dieses Skript ist ein Web-Crawler, der Rezept-Seiten auf Chefkoch.de durchläuft, um Rezept-Links zu sammeln.
Es verwendet BeautifulSoup, um HTML-Inhalte zu analysieren und requests, um Webseiten abzurufen.
Es filtert Rezepte aus und speichert die gesammelten Links in einer Textdatei.
"""

import os
import requests
from bs4 import BeautifulSoup

# Zielseite: https://www.chefkoch.de/rs/s0t14/Asiatisch-Rezepte.html

# Maximale Anzahl von Seiten, die durchsucht werden sollen
MAX_PAGES = 25

class Recipe_Crawler:
    # Initialisierung der Klasse mit den Parametern für die URL-Struktur und maximale Seitenanzahl
    def __init__(self, url_pre_page: str, page: int, url_past_page: str, max_pages: int):
        self.url_pre_page = url_pre_page
        self.page = page
        self.url_past_page = url_past_page
        self.search_base_url = self.build_base_url(url_pre_page, page, url_past_page)
        self.crawled_pages = []
        self.recipe_links = []
        self.max_pages = max_pages
    
    # Funktion zum Sammeln von Links von Chefkoch
    def collect_links(self, base_url) -> list:
        # Überprüfen, ob die aktuelle Seite nicht bereits durchsucht wurde und ob die maximale Seitenanzahl noch nicht erreicht ist
        if base_url not in self.crawled_pages and self.page < self.max_pages:
            #print(f'Request {base_url} ...')
            base_html_content = requests.get(base_url).text

            # Retrieving recipe cards
            soup_base_html_content = BeautifulSoup(base_html_content, 'html.parser')
            recipe_cards = soup_base_html_content.find_all(class_='ds-recipe-card')

            # Collecting links from recipe cards
            for card in recipe_cards:
                if(self.is_valid_recipe(card)):
                    link = card.find('a')['href']
                    self.recipe_links.append(link)
                    print(f'URLs collected:    {len(self.recipe_links)}')

            self.crawled_pages.append(base_url)

            self.page += 1
            self.search_base_url = self.build_base_url(self.url_pre_page, self.page, self.url_past_page)

            return self.collect_links(self.search_base_url)

        else:
            return self.recipe_links
        
    def is_valid_recipe(self, card):
        if card['data-vars-payed-content-type']=='plus_recipe':
            #print(f'PLUS RECIPE FOUND! ---> {card.find('a')['href']}')
            return False
        elif 'recipe-campaign' in card['data-vars-campaign-id']:
            #print(f'COMMERCIAL RECIPE FOUND! ---> {card.find('a')['href']}')
            return False
        else:
            return True

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
    rc = Recipe_Crawler('https://www.chefkoch.de/rs/', 0, 't14/Asiatisch-Rezepte.html', max_pages = MAX_PAGES)
    recipe_links = rc.collect_links(rc.search_base_url)
    
    for link in recipe_links:
        print(link)
    print(f'{len(recipe_links)} Links have been collected.')

    rc.save_target_urls(recipe_links)