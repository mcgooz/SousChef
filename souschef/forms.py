from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, ModelChoiceField, IntegerField

from .models import User, UserDashboard, Ingredient, FoodType, Recipe, Pantry, PantryIngredient, IngredientPerRecipe


class NewRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "ingredients", "steps", "image", "public"]
        widgets = {
            "name": Textarea(attrs={"rows": 1, "class": "textarea custom-input"}),
            "description": Textarea(attrs={"cols": 80, "rows": 3, "class": "custom-input"}            ),
            "image": Textarea(attrs={"rows": 1, "class": "textarea custom-input"}),
        }


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]
        widgets = {
            "name": TextInput(attrs={"required": "required"}),
        }

class PantryIngredientForm(ModelForm):
    name = ModelChoiceField(
        queryset=Ingredient.objects.all(),
        to_field_name="name",
    )
    ingredient_id = IntegerField()
    category = ModelChoiceField(queryset=FoodType.objects.all(), to_field_name="category")

    class Meta:
        model = PantryIngredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            "quantity": NumberInput(attrs={"required": "required"}),
            "unit": Select(attrs={"required": "required"}),
        }

class IngredientPerRecipeForm(ModelForm):
    class Meta:
        model = IngredientPerRecipe
        fields = ['ingredient', 'amount', 'unit']
        widgets = {
            "ingredient": Select(attrs={"required": "required"}),
            "amount": NumberInput(attrs={"required": "required"}),
            "unit": Select(attrs={"required": "required"}),
        }