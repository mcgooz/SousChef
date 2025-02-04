from django.core.cache import cache
from django.http import JsonResponse

from dotenv import load_dotenv
import os
import requests


from decimal import Decimal

from .models import Ingredient, Unit, IngredientPerRecipe

load_dotenv()

API_KEY = os.getenv("API_KEY")

### Query API or cache
def run_query(query):
    try:
        item = Ingredient.objects.get(name=query)
        print(f"ITEM FOUND: {item.name} ID: {item.ingredient_id}")
        results = [{"name": item.name, "id": item.ingredient_id}]
        
    except Ingredient.DoesNotExist:
        search = item_search(query)
        results = [{"name": item["name"], "id": item["id"]} for item in search]

    return JsonResponse({
        "results": results
        })


### API Search
def item_search(s):
    # Check if item is already in cache and return result (to avoid too many API calls)

    results = cache.get(f"item_search_{s}")
    if results:
        print("SEARCH RETRIEVED FROM CACHE")
        return results 
    
    # # Otherwise, search via API
    else:
        response = requests.get(f"https://api.spoonacular.com/food/ingredients/search?apiKey={API_KEY}&query={s}&number=10").json()

        results = response.get("results", [])
        
        print(f"API REQUEST")
        cache.set(f"item_search_{s}", results)
        print("SEARCH CACHED")
        return results
    
### Ingredient details API search
def detailed_search(id):
    details = cache.get(f"item_details_{id}")
    if details:
        print("DETAILS RETRIEVED FROM CACHE")
    
    else:
        response = requests.get(f"https://api.spoonacular.com/food/ingredients/{id}/information?apiKey={API_KEY}&amount=1").json()
        details = response.get("aisle")
        cache.set(f"item_details_{id}", details)
        print("DETAILS CACHED")
    
    print(details)
    return details
    

### Save or retrieve ingredient from DB
def fetch_or_create_ingredient(ingredient_input, item_id):
    ingredient, created = Ingredient.objects.get_or_create(
    name=ingredient_input,
    ingredient_id=item_id
    )
    print(f"FETCH_OR_CREATE: {ingredient}, {ingredient.ingredient_id}")
    return ingredient


### Sort by Categories
# def get_ingredient(categories, contents):
#     item_by_category = {}
#     for category in categories:
#         item = contents.filter(name__category=category)
#         item_by_category[category] = item

#     return item_by_category


### Table data
def get_table_data(contents):
    
    table_data = []
    for item in contents:
        row = [
            item.name.name.title(),  # Ingredient name
            item.quantity,   # Ingredient quantity
            item.unit,   # Unit name (assuming there's a unit field)
            item.id
        ]
        table_data.append(row)
    
    return table_data


### Convert to milli-units
def convert_to_milli(quantity, unit):
    if unit.unit_type == "l":
        return quantity * 1000, Unit.objects.get(unit_type="ml")
    elif unit.unit_type == "kg":
        return quantity * 1000, Unit.objects.get(unit_type="g")
    else:
        return quantity, unit
    

### Convert to appropriate unit
def change_unit(quantity, unit):
    if quantity >= 1000:
        if unit.unit_type == "mg":
            return Unit.objects.get(unit_type="g")
        elif unit.unit_type == "g":
            return Unit.objects.get(unit_type="kg")
        elif unit.unit_type == "ml":
            return Unit.objects.get(unit_type="l")
    else:
        return unit
    
    
### Return unit as decimal measure (kg,l) if more than 1000   
def check_quantity(total_quantity):
    if total_quantity >= 1000:
        new = total_quantity / 1000
        return new
    else:
        return total_quantity
    
   
def convert_from_ml(quantity):
    if quantity >= 1000:
        return quantity / 1000
    else:
        return quantity
    

### Update ingredient
def update_ingredient(i, q, u):

    # Convert current quantity to milli-units
    convert_current_quantity, convert_current_unit = convert_to_milli(Decimal(i.quantity), i.unit)
    
    
    # Convert new quantity to milli-units
    convert_new_quantity, convert_new_unit = convert_to_milli(q, u)
    

    # Calculate total quantity in milli-units
    total_quantity = Decimal(convert_current_quantity) + Decimal(convert_new_quantity)
 

    # Check for milli-unit measure over 1000 and convert unit (g to kg, ml to l)
    new_unit = change_unit(total_quantity, convert_new_unit)     
    i.unit = new_unit

    
    # Check and set correct decimal
    quantity_check = check_quantity(total_quantity)
    i.quantity = quantity_check


    print(f"CURRENT IN MILLI: {convert_current_quantity}")
    print(f"NEW IN MILLI: {convert_new_quantity}")
    print(f"TOTAL: {total_quantity}")
    print(f"CONVERT CURRENT UNIT: {convert_current_unit}")
    print(f"CONVERT NEW UNIT: {convert_new_unit}")
    print(f"QUANTITY CHECK: {i.quantity}")

    return i


def add_recipe_ingredient(r, i, a, u):
    ingredient_to_add = IngredientPerRecipe(
        recipe = r,
        ingredient = i,
        amount = a,
        unit = u
    )

    ingredient_to_add.save()


def crop_image(image):
    width, height = image.size
 
    new_dimension = min(width, height)
    left = (width - new_dimension) / 2
    top = (height - new_dimension) / 2
    right = (width + new_dimension) / 2
    bottom = (height + new_dimension) / 2
    
    return image.crop((left, top, right, bottom))