from dotenv import load_dotenv
import os
import requests

from decimal import Decimal

from .models import Ingredient, Unit, FoodType, PantryIngredient

load_dotenv()

API_KEY = os.getenv("API_KEY")

### API Search
def item_search(s):
    # Check if item is already in database and return result (to avoid too many API calls)
    # if Ingredient.objects.filter(name=s).exists():
    #     results = [{"name": s}]
    #     return results
    
    # # Otherwise, search via API

    response = requests.get(f"https://api.spoonacular.com/food/ingredients/search?apiKey={API_KEY}&query={s}&number=10").json()

    results = response.get("results", [])
    
    print(f"API REQUEST")
    print(results)
    return results
    
### Ingredient details API
def detailed_search(id):

    response = requests.get(f"https://api.spoonacular.com/food/ingredients/{id}/information?apiKey={API_KEY}&amount=1").json()

    print(response)


    details = response.get("categoryPath")
    if details and len(details) > 1:
            details = details[1]
    elif details:
        details = details[0]
    elif not details:
        details = response.get("originalName")

    return details
    

### Save or retrieve ingredient from DB
def fetch_or_create_ingredient(ingredient_input, category, item_id):
    category, created = FoodType.objects.get_or_create(category=category)
    ingredient, created = Ingredient.objects.get_or_create(
    name=ingredient_input,
    category=category,
    ingredient_id=item_id
    )
    print(ingredient)
    return ingredient


### Sort by Categories
def get_item_by_category(categories, contents):
    item_by_category = {}
    for category in categories:
        item = contents.filter(name__category=category)
        item_by_category[category] = item

    return item_by_category


### Table data
def get_table_data(items):
    max_items = max(len(item) for item in items.values())
    
    table_data = []
    for i in range(max_items):
        row = []
        for category, item in items.items():
            if i < len(item):
                row.append(item[i])
            else:
                row.append(None)
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