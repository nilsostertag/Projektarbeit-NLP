from dataclasses import asdict, dataclass
from typing import List
import os
import bs4
import json

@dataclass
class Dish_time:
    prep: int
    cook : int
    sum_time: int

@dataclass
class Nutritional_values:
    kcal: int
    protein: str
    fat: str
    carbs: str

@dataclass
class Properties:
    date_published: int
    rating: float
    difficulty: str
    nutritional_values: List[Nutritional_values]
    dish_time: Dish_time
    tags: List[str]

    #def __post_init__(self):
        #self.nutritional_values = Nutritional_values(**self.nutritional_values)
        #self.dish_time = Dish_time(**self.dish_time)
        #self.tags = List[str](**self.tags)

@dataclass
class Ingredient_payload:
    name: str
    amount: int
    unit: str

@dataclass
class Ingredients:
    portions: int
    payload: List[Ingredient_payload]

@dataclass
class Recipe:
    region: str
    recipe_id: str
    url: str
    region: str
    title: str
    author: str
    properties: Properties
    ingredients: Ingredients
    preparation: str


@dataclass
class Recipes:
    payload: List[Recipe]

    def to_json(self):
        return json.dumps(asdict(self), indent = 2, ensure_ascii=False)

    #def __post_init__(self):
        #self.properties = Properties(**self.properties)
        #self.ingredients = [Ingredient(**ingredient) for ingredient in self.ingredients]

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Data structure for recipe scraping process
@dataclass
class Recipe_HTML_preprocessed:
    region: str
    url: str
    header: bs4.element.Tag
    ingredients: bs4.element.Tag
    nutrition: bs4.element.Tag
    preparation: bs4.element.Tag
    tags: bs4.element.Tag
    author: bs4.element.Tag

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class Regional_urls:
    region: str
    count: int
    urls: List[str]
    
@dataclass
class Regional_URL_Collection:
    payload: List[Regional_urls]

    def to_json(self):
        return json.dumps(asdict(self), indent = 2, ensure_ascii=False)