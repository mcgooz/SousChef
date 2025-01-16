from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import NewRecipeForm, IngredientPerRecipeFormSet
from .models import Recipe, IngredientPerRecipe


def add_recipe_get_request(request):  
    recipe_form = NewRecipeForm()
    ingredient_formset = IngredientPerRecipeFormSet(queryset=IngredientPerRecipe.objects.none()) 

    return render(request, "SousChef/add_recipe.html", {
        "recipe_form": recipe_form,
        "ingredient_formset": ingredient_formset
    })


def add_recipe_post_request(request):
    recipe_form = NewRecipeForm(request.POST)

    if recipe_form.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.created_by = request.user
        recipe.title = recipe.title.title()
        if Recipe.objects.filter(title=recipe.title).exists():
            return JsonResponse({"rename": "This recipe already exists. Please choose another"})
        else:
            recipe.save()
        
        ingredient_formset = IngredientPerRecipeFormSet(request.POST)
        if ingredient_formset.is_valid(): 
            for form in ingredient_formset:   
                    ingredient_instance = form.save(commit=False)
                    ingredient_instance.recipe = recipe
                    ingredient_instance.save()
        else:
            print(ingredient_formset.errors)

        return redirect("add_recipe")
