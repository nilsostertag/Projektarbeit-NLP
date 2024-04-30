from typing import List
import os
import bs4
import data_export as de
import json

# Target data structure for raw scraped data
class Dish_Time:
    def __init__(self, prep: int, cook: int, sum_time: int):
        self.prep = prep
        self.cook = cook
        self.sum_time = sum_time

class Nutritional_Val:
    def __init__(self, kcal: int, protein, fat, carbs):
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

class Properties:
    def __init__(self, date_published: str, nutritional_val: Nutritional_Val, dish_time: Dish_Time, tags: List[str]):
        self.date_published = date_published
        self.nutritional_values = nutritional_val
        self.dish_time = dish_time
        self.tags = tags

class Ingredient:
    def __init__(self, name: str, amount: int, unit: str):
        self.name = name
        self.amount = amount
        self.unit = unit

class Recipe:
    def __init__(self, recipe_id: str, link: str, title: str, author: str, properties: Properties, ingredients: List[Ingredient], article: str):
        self.id = recipe_id
        self.link = link
        self.title = title
        self.author = author
        self.properties = properties
        self.ingredients = ingredients
        self.article = article

# Data structure for recipe scraping process
class Recipe_HTML_preprocessed:
    def __init__(self, url, header: bs4.element.Tag, ingredients: bs4.element.Tag, nutrition: bs4.element.Tag, preparation: bs4.element.Tag):
        self.url = url
        self.header = header
        self.ingredients = ingredients
        self.nutrition = nutrition
        self.preparation = preparation


if __name__ == '__main__':
    sample = Recipe(
        link = 'https://www.chefkoch.de/rezepte/2826671434712499/Haehnchen-suesssauer-wie-im-Chinarestaurant.html',
        recipe_id = '2826671434712499',
        title = 'Hähnchen süß-sauer wie im Chinarestaurant',
        author = 'NatuerlichLecker',
        properties = Properties(
            date_published = '25012018',
            nutritional_val = Nutritional_Val(
                kcal = 672,
                protein = 27.39,
                fat = 7.63,
                carbs = 121.27
            ),
            dish_time = Dish_Time(
                prep = 25,
                cook = 30,
                sum_time = 55
            ),
            tags = ['Asien', 'Fleisch', 'Gemüse', 'Hauptspeise', 'Reis', 'Geflügel', 'Braten', 'China', 'Frucht', 'Getreide']
        ),
        ingredients = [
            Ingredient(
            name = 'Reis',
            amount = 250,
            unit = 'g'
            ),
            Ingredient(
            name = 'Hähnchenbrüste',
            amount = 2,
            unit = ''
            ),
            Ingredient(
            name = 'Ei(er)',
            amount = 1,
            unit = ''
            ),
            Ingredient(
            name = 'Speisestärke',
            amount = 4,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Ananas',
            amount = 1,
            unit = 'Dose'
            ),
            Ingredient(
            name = 'Apfelessig oder Weinessig',
            amount = 7,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Zucker',
            amount = 4,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Salz',
            amount = 1,
            unit = 'TL'
            ),
            Ingredient(
            name = 'Ketchup',
            amount = 2,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Sojasauce',
            amount = 2,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Öl, neutrales (z.B. Sonnenblumenöl)',
            amount = 2,
            unit = 'EL'
            ),
            Ingredient(
            name = 'Zwiebel(n)',
            amount = 1,
            unit = ''
            ),
            Ingredient(
            name = 'Paprikaschote(n)',
            amount = 2,
            unit = ''
            )
        ],
        article = 'Heute machen wir leckeres Hähnchen süßsauer wie vom Chinamann. Als ich noch jünger war, also Ende der Neunziger bzw. Anfang der Zweitausender Jahre war chinesisches Essen voll im Trend und und Chinarestaurants inklusive Lieferdienst schossen an jeder Ecke wie Pilze aus dem Boden. Nun, 10 - 15 Jahre später, habe ich mich entschlossen diese Variante des damals auch bei mir so beliebten Hähnchen süßsauer zu kreieren. Viel Spaß mit dem Rezept. Zuerst wird der Reis mit etwas Salz gekocht, im Video wird Naturreis genommen, dieser hat eine Garzeit von ca. 35 Minuten. Die Hühnerbrüste werden gewaschen und in mundgerechte Stücke geschnitten. Nun wird ein Ei in eine kleine Schüssel gegeben mit Pfeffer und Salz gewürzt und verquirlt. In eine weitere Schüssel werden 2 EL Speisestärke gegeben und etwas mit dem Löffel verteilt. Eine Pfanne wird aufgeheizt. Nun werden die Hühnerbruststücke in die Stärke gegeben und mehrmals gedreht, bis sie vollständig bedeckt sind. Danach werden sie zum Ei gegeben und ebenfalls gedreht bis sie vollständig mit dem Ei überzogen sind. Jetzt wird das mit Ei überzogene Fleisch in einer Pfanne rundherum gebraten bis es gar ist. Danach wird es auf einen Teller gegeben und beiseitegestellt. Als nächstes wird die Ananas aus der Dose abgetropft und die Flüssigkeit aus der Dose aufgefangen. Für die Sauce wird der Essig mit Zucker, Salz, Sojasauce, Öl und Ketchup in eine Schüssel gegeben und durchgerührt. Die Zwiebel wird geputzt, halbiert und in feine Ringe geschnitten und in der Pfanne, in der die Hähnchenstücke waren, angebraten. Nun werden noch 2 Paprikaschoten geputzt und ebenfalls in mundgerechte Stücke geschnitten. Diese werden dann mit der Ananas zu den Zwiebeln gegeben und 5 Minuten mitgebraten. Dann wird die Sauce dazu gegeben und alles weitere 3 Minuten auf mittlerer Hitze geköchelt. In der Zwischenzeit werden die letzten 2 EL Speisestärke mit ca. 80 Milliliter des Ananassaftes angerührt und dann in die Pfanne gegeben. Danach wird alles wieder auf dem Herd geben um etwas zu reduzieren. Inzwischen sollte der Reis fertig sein. Dieser wird abgegossen und kurz beiseitegestellt, denn jetzt wird das Fleisch zum Gemüse in die Pfanne gegeben um rasch wieder heiß zu werden. Dann wird der Reis auf die Teller verteilt, Hähnchen und Gemüse darauf angerichtet und etwas Sauce darauf gegossen.'
    )

    export_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'scraped', 'sample.json')
    de.export_to_json(obj = sample, path = export_path, encoder = de.RecipeEncoder)