from typing import List
import bs4

# Target data structure for raw scraped data
class Dish_Time:
    def __init__(self, prep: int, cook: int, sum_time: int):
        self.prep = prep
        self.cook = cook
        self.sum_time = sum_time

class Nutritional_Val:
    def __init__(self, kcal: int, protein: int, fat: int, carbs: int):
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

class Properties:
    def __init__(self, date_published: str, nutritional_val: Nutritional_Val, dish_time: Dish_Time, tags: List[int]):
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