# Datenstruktur für Chefkoch-Rezepte

Array an JSON-Objekten

struct recipe
- id
- title
- author
- properties
    - date_published
    - nutritional_values
        - kcal
        - protein
        - fat
        - carbs
    - dish_time
        - prep
        - cook
        - sum
    - tags
- List(ingredients)
    - name
    - amount
    - unit
- article