from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import Pantry, PantryIngredient
from .forms import PantryIngredientForm

from decimal import Decimal
import json

from .utils import *


### Handle GET requests
def pantry_get_request(request):
    query = request.GET.get("query")

    # Search API or database
    if query:
        return run_query(query)
    
    form = PantryIngredientForm()          
    pantry = Pantry.objects.filter(user=request.user)
    contents = PantryIngredient.objects.filter(pantry__in=pantry).order_by('name__name')
    
    if contents:
        table_data = get_table_data(contents)
        return render(request, "SousChef/pantry.html", {
            "pantry": pantry,
            "table_data": table_data,
            "form": form, 
        })

    else:
        return render(request, "SousChef/pantry.html", {
            "pantry": pantry,
            "form": form, 
        })


### Handle POST requests
def pantry_post_request(request):

    pantry = Pantry.objects.get(user=request.user)
    form = PantryIngredientForm(request.POST)
    
    if form.is_valid():
        ingredient_input = form.cleaned_data["name"]
        ingredient_id = form.cleaned_data["ingredient_id"]
        quantity_input = form.cleaned_data["quantity"]
        unit_id = form.cleaned_data["unit"]

        ingredient = fetch_or_create_ingredient(ingredient_input, ingredient_id)
        
        pantry_ingredient = PantryIngredient.objects.filter(pantry=pantry, name=ingredient).first()
        
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


def add_to_pantry(n, q, u, p):
    pantry_ingredient= PantryIngredient(
        name=n,
        quantity=q,
        unit=u,
        pantry=p,
    )

    pantry_ingredient.save()