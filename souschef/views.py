from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import User, UserDashboard, Pantry, Recipe
from .forms import NewRecipeForm, IngredientForm, PantryIngredientForm, IngredientPerRecipeFormSet

import datetime, json

from .pantry_view import *
from .add_recipe_view import *

### Homepage
def index(request):
    today = datetime.datetime.today().date()
    date = datetime.datetime.strftime(today, '%a %d %b %Y')
    
    return render(request, "SousChef/index.html", {
        "date": date,
    })

### User dashboard
def user_dashboard(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserDashboard.objects.get(user_name=current_user)

        return render(request, "SousChef/user_dashboard.html", {
            "profile": profile,
        })
    

### Recipes View
def recipes(request):
    recipes = Recipe.objects.all()
    for recipe in recipes:
        print(f"RECIPE_INGREDIENTSET: {recipe.ingredientperrecipe_set.all()}")
    return render(request, "SousChef/recipes.html", {
            "recipes": recipes,
        }) 
    

### Pantry View
def pantry(request):
    if request.method == "GET":
        return pantry_get_request(request)
    
    elif request.method == "POST":
        return pantry_post_request(request)
    

### Add a Recipe View
def add_recipe(request):
    if request.method == "GET":
        return add_recipe_get_request(request)

    elif request.method == "POST":
        return add_recipe_post_request(request)
        
        
### Ingredient Lookup
def ingredient_details(request):
    if request.method == "POST":
        item = json.loads(request.body)
        item_name = item.get("name")
        item_id = item.get("id")

        ingredient_details = detailed_search(item_id)
        ingredient = fetch_or_create_ingredient(item_name, item_id)
        ingredient_dict = {
            "name": ingredient.name,
            "id": ingredient.id,
        }
        details = {
            "ingredient": ingredient_dict,
            "ingredient_details": ingredient_details
        }
        print(f"INGREDIENT DETAILS-FETCH_OR_CREATE {ingredient}")
        return JsonResponse({ "details": details})


### Login View
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"].title()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "SousChef/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "SousChef/login.html")
    
### Logout View   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


### Register View
def register(request):
    if request.method == "POST":
        username = request.POST["username"].title()
        if not username:
            return render(request, "SousChef/register.html", {
                "message": "Please enter a username!"
            })
        
        email = request.POST["email"]
        if not email:
            return render(request, "SousChef/register.html", {
                "message": "Please enter an email address!"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "SousChef/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and profile and pantry
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = UserDashboard.objects.create(user_name=user)
            profile.save()
            pantry = Pantry.objects.create(user=user)
            pantry.save()
        except IntegrityError:
            return render(request, "SousChef/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "SousChef/register.html")


# def recipe_ingredient(request):
#     if request.method == "POST":
#         print("RECIPE INGREDIENT")
        
#         ingredient_input = request.POST.get("ingredient")
#         ingredient_id = request.POST.get("ingredientId")
#         ingredient_check = fetch_or_create_ingredient(ingredient_input, ingredient_id)
#         form_data = request.POST.copy()
        
#         form = IngredientPerRecipeFormSet(form_data)
#         if form.is_valid():
#             ingredient = ingredient_check
#             amount = form.cleaned_data["amount"]
#             unit_id = form.cleaned_data["unit"]
#             unit = Unit.objects.get(unit_type=unit_id)
#             add_ingredient = {"ingredient": ingredient.name, "amount": amount, "unit": unit.unit_type, "ingredient_id": ingredient_id}
#             return JsonResponse(add_ingredient)
                
#         else:
#             print(f"RECIPE_INGREDIENT VIEW {form.errors}")

#     return HttpResponseRedirect(reverse("add_recipe"))