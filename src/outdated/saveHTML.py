import requests

setup_file = open('data/urls_to_scrape.txt', 'r')
URLs_to_scrape = setup_file.readlines()

for url in URLs_to_scrape:

    #URL = 'https://www.chefkoch.de/magazin/artikel/2477,0/Chefkoch/Cordon-bleu-Schnitzel-fuer-Fortgeschrittene.html'
    page = requests.get(url)

    article = url.split('/')[-1].split('.')[0]

    print(article)

    filename = f'export_{article}'

    with open(f'data/scraping/{filename}.html', 'wb+') as file:
        file.write(page.content)

print('done.')