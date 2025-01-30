from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .forms import NewRecipeForm, StepFormSet, IngredientPerRecipeFormSet
from .models import Recipe, IngredientPerRecipe
from PIL import Image

from .utils import crop_image


def add_recipe_get_request(request):
    StepFormSet.extra = 1
    IngredientPerRecipeFormSet.extra = 1
    
    recipe_form = NewRecipeForm()
    step_formset = StepFormSet()
    ingredient_formset = IngredientPerRecipeFormSet(queryset=IngredientPerRecipe.objects.none()) 

    return render(request, "SousChef/add_recipe.html", {
        "recipe_form": recipe_form,
        "step_formset": step_formset,
        "ingredient_formset": ingredient_formset
    })


def add_recipe_post_request(request):
    recipe_form = NewRecipeForm(request.POST, request.FILES)
    step_formset = StepFormSet(request.POST)

    if recipe_form.is_valid() and step_formset.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.created_by = request.user
        recipe.title = recipe.title.title()

        if Recipe.objects.filter(title=recipe.title).exists():
            return JsonResponse({"rename": "This recipe already exists. Please choose another name"})
        else:
            recipe.save()
            if recipe.image:
                image = Image.open(recipe.image.path)
                cropped_image = crop_image(image)
                cropped_image.save(recipe.image.path)

        steps = step_formset.save(commit=False)
        for step in steps:
             step.recipe = recipe
             step.save()


        ingredient_formset = IngredientPerRecipeFormSet(request.POST)
        if ingredient_formset.is_valid(): 
            for form in ingredient_formset:   
                    ingredient_instance = form.save(commit=False)
                    ingredient_instance.recipe = recipe
                    ingredient_instance.save()
        else:
            print(ingredient_formset.errors)

    else:
        print(recipe_form.errors)
        print(step_formset.errors)

    return render(request, "souschef/recipe.html", {
        "recipe": recipe
    })
