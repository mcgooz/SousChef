from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, ModelChoiceField

from .models import User, UserDashboard, Ingredient, Recipe, Pantry, PantryIngredient, IngredientPerRecipe


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
        fields = ["name", "category"]
        widgets = {
            "name": TextInput(attrs={"required": "required"}),
            "category": Select(attrs={"required": "required"}),
        }

class PantryIngredientForm(ModelForm):
    name = ModelChoiceField(queryset=Ingredient.objects.all(), widget=Select(attrs={"required": "required"}))
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