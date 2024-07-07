from typing import List
import random
import data_structures as ds


class randomizer:
    def __init__(self):
        self.returned_ids = []

    def get_random_recipe(self, list: List[ds.Recipe], enable_returning_duplicates: bool = False):
        random_index = random.randint(0, len(list))
        if enable_returning_duplicates and list[random_index].recipe_id in self.returned_ids:
            self.get_random_recipe(list, enable_returning_duplicates)
        self.returned_ids.append(list[random_index].recipe_id)
        return list[random_index]