from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import User, UserDashboard, Pantry
from .forms import NewRecipeForm, IngredientForm, PantryIngredientForm, IngredientPerRecipeForm

import datetime, json

from .pantry_utils import *


def index(request):
    today = datetime.datetime.today().date()
    date = datetime.datetime.strftime(today, '%a %d %b %Y')
    
    return render(request, "SousChef/index.html", {
        "date": date,
    })



def user_dashboard(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile = UserDashboard.objects.get(user_name=current_user)

        return render(request, "SousChef/user_dashboard.html", {
            "profile": profile,
        })
    

### Pantry View
def pantry(request):
    if request.method == "GET":
        return pantry_get_request(request)
    
    elif request.method == "POST":
        return pantry_post_request(request)
    

### Recipe View
def recipes(request):
    if request.method == "POST":
        recipe_form = NewRecipeForm(request.POST)
        ingredient_formset = IngredientPerRecipeForm()

        if recipe_form.is_valid():
            recipe = recipe_form.save()
            
            return redirect("recipes")
    else:
        recipe_form = NewRecipeForm()        
        ingredient_formset = IngredientPerRecipeForm()
        

    return render(request, "SousChef/recipes.html", {
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset
        })


def ingredient_details(request):
    if request.method == "POST":

        item = json.loads(request.body)
        item_name = item.get("name")
        item_id = item.get("id")
        print(item_name, item_id)
        category = detailed_search(item_id)
        print(f"CATEGORY: {category}")
        fetch_or_create_ingredient(item_name, category, item_id)
        return JsonResponse({ "category": category})


def recipe_ingredient(request):
    if request.method == "POST":
        
        ingredient_input = request.POST.get("ingredient")
        category = FoodType.objects.get(id=request.POST.get("category"))
        ingredient = fetch_or_create_ingredient(ingredient_input, category)
        form_data = request.POST.copy()
        form_data["name"] = ingredient.id
        form = IngredientPerRecipeForm(form_data)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            unit = form.cleaned_data["unit"]
            
            print(ingredient, category, amount, unit)
        else:
            print(form.errors)

    return HttpResponseRedirect(reverse("recipes"))


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
