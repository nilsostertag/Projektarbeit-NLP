class Recipe:
    def __init__(self, recipe_id, title, author, properties, ingredients, article):
        self.id = recipe_id
        self.title = title
        self.author = author
        self.properties = properties
        self.ingredients = ingredients
        self.article = article

class Properties:
    def __init__(self, date_published, nutritional_val, dish_time, tags):
        self.date_published = date_published
        self.nutritional_values = nutritional_val
        self.dish_time = dish_time
        self.tags = tags

class Nutritional_Val:
    def __init__(self, kcal, protein, fat, carbs):
        self.kcal = kcal
        self.protein = protein
        self.fat = fat
        self.carbs = carbs

class Dish_Time:
    def __init__(self, prep, cook, sum_time):
        self.prep = prep
        self.cook = cook
        self.sum_time = sum_time