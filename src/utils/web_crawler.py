import requests
from bs4 import BeautifulSoup

class web_crawler:

    def __init__(self, url:str, page:int, search_argument:str, ending:str):
        self.search_base_url = f'{url}/rs/s{page}/{search_argument}/{ending}.html'

    def collect_links(self, url):
        self.base_html_content = requests.get(url).text

        soup = BeautifulSoup(self.base_html_content, 'html.parser')

        self.recipe_cards = soup.find_all(class_='ds-recipe-card__link ds-teaser-link')

        for card in self.recipe_cards:
            print(card.text.strip())


if __name__ == '__main__':
    wc = web_crawler('https://www.chefkoch.de', 0, 'proteine', 'Rezepte')
    wc.collect_links(wc.search_base_url)

