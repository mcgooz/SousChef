from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import User, UserDashboard, Pantry, Recipe, Ingredient, Favourite
from .forms import NewRecipeForm, IngredientForm, PantryIngredientForm, IngredientPerRecipeFormSet, UserDashboardForm

import datetime, json, random

from .pantry_view import *
from .add_recipe_view import *


### Homepage
def index(request):
    recipes = Recipe.objects.all()
    if recipes:
        random_recipe = random.choice(recipes)
    else: 
        random_recipe = None
    
    return render(request, "SousChef/index.html", {
        "random_recipe": random_recipe
    })


### Main Search
def home_search(request):
    
    if 'word' in request.GET:
        word = request.GET.get('word')
        recipes = Recipe.objects.filter(
            Q(title__icontains=word) | Q(ingredients__name__icontains=word)
            ).values('title', 'id').distinct()
        recipe_result = list(recipes)

        return JsonResponse({"recipe_result": recipe_result})
 

### User dashboard
@login_required
def user_dashboard(request):
    current_user = request.user
    profile = UserDashboard.objects.get(user_name=current_user)
    recipes = Recipe.objects.filter(created_by=current_user)
    form = UserDashboardForm()
    recipe_form = NewRecipeForm()
    favourites = Favourite.objects.filter(user=profile)

    if request.method == "GET":

        return render(request, "souschef/user_dashboard.html", {
            "profile": profile,
            "recipes": recipes,
            "favourites": favourites,
            "form": form,
            "recipe_form": recipe_form
        })
    
    elif request.method == "POST":
        profile.profile_picture.delete()
        image = request.FILES.get("croppedImage")
        profile.profile_picture.save(image.name, image)
        return JsonResponse({"message": "Picture updated successfully!"})


### Favourites
@login_required  
def favourite(request, id):
    if request.method == "POST":
        current_user = UserDashboard.objects.get(user_name=request.user)
        recipe = Recipe.objects.get(id=id)
        status = Favourite.objects.filter(user=current_user, favourite_recipe=recipe).exists()
        if status:
            Favourite.objects.filter(user=current_user, favourite_recipe=recipe).delete()
            favourite = False
        else:
            Favourite.objects.create(user=current_user, favourite_recipe=recipe)
            favourite = True
        
        return JsonResponse({"favourite": favourite})


### Update Recipe Image
@login_required
def update_recipe_image(request):
    recipe_id = request.POST.get("recipeID")
    image = request.FILES.get("croppedImage")
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.image.delete()

    recipe.image.save(image.name, image)
    print(f"Image for recipe {recipe} updated")

    return JsonResponse({"message": "Image updated successfully!"})
    

### Recipes View
def recipes(request):
    recipes = Recipe.objects.all()

    return render(request, "SousChef/recipes.html", {
            "recipes": recipes,
        })


### Detailed Recipe View
def recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    if request.user.is_authenticated:
        current_user = UserDashboard.objects.get(user_name=request.user)
        favourite = Favourite.objects.filter(user=current_user, favourite_recipe=recipe).exists()

        return render(request, "souschef/recipe.html", {
            "recipe": recipe,
            "favourite": favourite
        })
    
    else:
        return render(request, "souschef/recipe.html", {
            "recipe": recipe,
        })


### Pantry View
@login_required
def pantry(request):
    if request.method == "GET":
        return pantry_get_request(request)
    
    elif request.method == "POST":
        return pantry_post_request(request)
        
    
    
### Pantry Delete
@login_required
def pantry_delete(request):
    if request.method == "POST":
        pantry_item_id = request.POST.get("pantry_item_id")
        print(pantry_item_id)
        item = PantryIngredient.objects.get(id=pantry_item_id)
        item.delete()

        return HttpResponseRedirect(reverse("pantry"))


### Add a Recipe View
@login_required
def add_recipe(request):
    if request.method == "GET":
        return add_recipe_get_request(request)

    elif request.method == "POST":
        return add_recipe_post_request(request)


### Delete Recipe
@login_required
def delete_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    if recipe.created_by == request.user:
        
        if request.method == "POST":
            recipe.image.delete()
            recipe.delete()
            print(f"{recipe} deleted")

            return HttpResponseRedirect(reverse("user_dashboard"))
             
            
### Ingredient Lookup
@login_required
def ingredient_details(request):
    if request.method == "POST":
        item = json.loads(request.body)
        item_name = item.get("name")
        item_id = item.get("id")

        ingredient_details = detailed_search(item_id)
        ingredient = fetch_or_create_ingredient(item_name, item_id)

        # Save extra info to DB
        ingredient.ingredient_details = ingredient_details
        ingredient.save()
        
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


### Single Ingredient View
def ingredient(request, id):
    ingredient = Ingredient.objects.get(id=id)

    return render(request, "souschef/ingredient.html", {
        "ingredient": ingredient
    })


### Login View
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"].title()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return JsonResponse ({
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

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "SousChef/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user with corresponding profile and pantry
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


#### FUTURE UPDATES ####
def future():
    pass
    # ### Edit Recipe View
    # def edit_recipe(request, id):
    #     recipe = Recipe.objects.get(id=id)
    #     if recipe.created_by == request.user:

    #         if request.method == "GET":
    #             StepFormSet.extra = 0
    #             IngredientPerRecipeFormSet.extra = 0
        
    #             recipe_form = NewRecipeForm(instance=recipe)
    #             step_formset = StepFormSet(instance=recipe)
    #             ingredient_formset = IngredientPerRecipeFormSet(instance=recipe)

    #             return render(request, "souschef/edit_recipe.html", {
    #                 "recipe": recipe,
    #                 "recipe_form": recipe_form,
    #                 "step_formset": step_formset,
    #                 "ingredient_formset": ingredient_formset,
    #             })
        
    #     if request.method == "POST":

    #         recipe_form = NewRecipeForm(request.POST, request.FILES, instance=recipe)
    #         step_formset = StepFormSet(request.POST, instance=recipe)
    #         ingredient_formset = IngredientPerRecipeFormSet(request.POST, instance=recipe)

    #         if request.POST.get("action") == "save":
    #             print(request.POST)

    #             if recipe_form.is_valid():
                    
    #                 recipe = recipe_form.save(commit=False)
    #                 recipe.created_by = request.user
    #                 recipe.title = recipe.title.title()

    #                 if 'image-clear' in request.POST:
    #                     recipe.image.delete()
                    
    #                 recipe.save()

    #                 if recipe.image:
    #                     image = Image.open(recipe.image.path)
    #                     cropped_image = crop_image(image)
    #                     cropped_image.save(recipe.image.path)

    #                 if step_formset.is_valid():
    #                     steps = step_formset.save(commit=False)

    #                     for old_step in step_formset.deleted_forms:
    #                         old_step.instance.delete()

    #                     for step in steps:
    #                         step.recipe = recipe
    #                         step.save()

    #                     step_formset.save()

    #                 if ingredient_formset.is_valid():
    #                     ingredients = ingredient_formset.save(commit=False)
                            
    #                     for ing in ingredient_formset.deleted_objects:
    #                         print(f"Deleted Ingredient: {ing}")
    #                         ing.instance.delete()
                            
    #                     for ingredient_instance in ingredients:
    #                         ingredient_instance.recipe = recipe
    #                         ingredient_instance.save()
                        
    #                     ingredient_formset.save()

    #             return render(request, "souschef/recipe.html", { 
    #                 "recipe": recipe,
    #             })