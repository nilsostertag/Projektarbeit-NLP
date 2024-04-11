import requests

URL = 'https://www.chefkoch.de/rezepte/992101204469611/Thai-Red-Curry-fuer-mehrere-Variationen.html'
page = requests.get(URL)

with open('data/scraping/first_export.html', 'wb+') as file:
    file.write(page.content)

print('done.')