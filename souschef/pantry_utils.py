from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import Pantry, PantryIngredient, FoodType
from .forms import PantryIngredientForm

from decimal import Decimal

from .utils import *

### Query API or database via GET
def run_query(query):
    search = item_search(query)
    results = [{"name": item["name"]} for item in search]
    ids = [{"id": item["id"]} for item in search]
    print(ids)
    return JsonResponse({
        "results": results,
        "ids": ids
        })


### Handle GET requests
def pantry_get_request(request):
    query = request.GET.get("query")

    # Search API or database
    if query:
        return run_query(query)
    
    form = PantryIngredientForm()          
    pantry = Pantry.objects.filter(user=request.user)
    contents = PantryIngredient.objects.filter(pantry__in=pantry)
    categories = FoodType.objects.all()
    
    item_by_category = get_item_by_category(categories, contents)
    table_data = get_table_data(item_by_category)

    return render(request, "SousChef/pantry.html", {
        "pantry": pantry,
        "categories": categories,
        "table_data": table_data,
        "form": form, 
    })


### Handle POST requests
def pantry_post_request(request):

    # If the ingredient isn't in the DB, save it first
    ingredient_input = request.POST.get("name")
    category_id = FoodType.objects.get(id=request.POST.get("category"))
    print(f"INPUT = {ingredient_input} in {category_id}")


    ingredient = fetch_ingredient(ingredient_input, category_id)
    print(f"FETCHED = {ingredient}")


    form_data = request.POST.copy()
    form_data["name"] = ingredient.id
    pantry = Pantry.objects.get(user=request.user)
    form = PantryIngredientForm(form_data)

    if form.is_valid():
        ingredient = form.cleaned_data["name"]
        category_id = request.POST.get("category")
        quantity_input = form.cleaned_data["quantity"]
        unit_id = form.cleaned_data["unit"]

        pantry_ingredient = PantryIngredient.objects.filter(pantry=pantry, ingredient=ingredient).first()
        
        if pantry_ingredient:
            update = update_ingredient(pantry_ingredient, quantity_input, unit_id)
            update.save()
        else:
            add_to_pantry(ingredient, quantity_input, unit_id, pantry)

        return HttpResponseRedirect(reverse("pantry"))

    else:
        print(form.errors)
        error = "Please fill in all fields"
        return JsonResponse({"error": error})


def add_to_pantry(i, q, u, p):
    pantry_ingredient= PantryIngredient(
        ingredient=i,
        quantity=q,
        unit=u,
        pantry=p,
    )

    pantry_ingredient.save()