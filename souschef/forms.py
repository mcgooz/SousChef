from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, ModelChoiceField, IntegerField

from .models import User, UserDashboard, Ingredient, Recipe, Pantry, PantryIngredient, IngredientPerRecipe, Unit

from django.forms import inlineformset_factory


class NewRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "steps", "image", "public"]
        widgets = {
            "name": Textarea(attrs={"rows": 1, "class": "textarea custom-input"}),
            "description": Textarea(attrs={"cols": 40, "rows": 3, "class": "custom-input"}            ),
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
    # category = ModelChoiceField(queryset=FoodType.objects.all(), to_field_name="category")

    class Meta:
        model = PantryIngredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            "quantity": NumberInput(attrs={"required": "required"}),
            "unit": Select(attrs={"required": "required"}),
        }

IngredientPerRecipeFormSet = inlineformset_factory(
    Recipe,
    IngredientPerRecipe,
    fields = ['ingredient', 'amount', 'unit'],
    extra=1,
    can_delete=True,
    widgets = {
        "ingredient": TextInput(attrs={"required": "required", "class": "form-control search-box", "placeholder": "Search ingredients", "autocomplete": "off"}),
        "amount": NumberInput(attrs={"required": "required", "id": "amount", "class": "form-control"}),
        "unit": Select(attrs={"required": "required", "id": "unit", "class": "form-control form-select"}),
    },
)


# class IngredientPerRecipeForm(ModelForm):
#     ingredient = TextInput()
#     unit = ModelChoiceField(queryset=Unit.objects.all())

#     class Meta:
#         model = IngredientPerRecipe
#         fields = ['ingredient', 'amount', 'unit']
#         widgets = {
#             "ingredient": TextInput(attrs={"required": "required"}),
#             "amount": NumberInput(attrs={"required": "required"}),
#             "unit": Select(attrs={"required": "required"}),
#         }