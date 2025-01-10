from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import Pantry, PantryIngredient, FoodType
from .forms import PantryIngredientForm

from decimal import Decimal
import json

from .utils import *

### Query API or database via GET
def run_query(query):
    search = item_search(query)
    results = [{"name": item["name"]} for item in search]
    ids = [{"id": item["id"]} for item in search]
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
    
    if contents:
        item_by_category = get_item_by_category(categories, contents)
        table_data = get_table_data(item_by_category)
        return render(request, "SousChef/pantry.html", {
            "pantry": pantry,
            "categories": categories,
            "table_data": table_data,
            "form": form, 
        })

    else:
        return render(request, "SousChef/pantry.html", {
            "pantry": pantry,
            "categories": categories,
            "form": form, 
        })


### Handle POST requests
def pantry_post_request(request):

    pantry = Pantry.objects.get(user=request.user)
    form = PantryIngredientForm(request.POST)
    
    if form.is_valid():
        ingredient_input = form.cleaned_data["name"]
        ingredient_id = form.cleaned_data["ingredient_id"]
        category_input = form.cleaned_data["category"]
        quantity_input = form.cleaned_data["quantity"]
        unit_id = form.cleaned_data["unit"]

        ingredient = fetch_or_create_ingredient(ingredient_input, category_input, ingredient_id)
        
        pantry_ingredient = PantryIngredient.objects.filter(pantry=pantry, name=ingredient).first()
        
        if pantry_ingredient:
            update = update_ingredient(pantry_ingredient, quantity_input, unit_id)
            update.save()
        else:
            add_to_pantry(ingredient, category_input, quantity_input, unit_id, pantry)

        return HttpResponseRedirect(reverse("pantry"))

    else:
        print(form.errors)
        error = "Please fill in all fields"
        return JsonResponse({"error": error})


def add_to_pantry(n, c, q, u, p):
    pantry_ingredient= PantryIngredient(
        name=n,
        quantity=q,
        unit=u,
        pantry=p,
    )

    pantry_ingredient.save()