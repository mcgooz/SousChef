from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, ModelChoiceField, IntegerField, HiddenInput

from .models import User, UserDashboard, Ingredient, Recipe, Pantry, PantryIngredient, IngredientPerRecipe, Unit

from django.forms import inlineformset_factory


class NewRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "steps", "image", "public"]
        widgets = {
            "name": Textarea(attrs={"rows": 1, "class": "textarea custom-input"}),
            "description": Textarea(attrs={"cols": 40, "rows": 3, "class": "custom-input"}),
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

# class IngredientPerRecipeForm(ModelForm):
#     class Meta:
#         model = IngredientPerRecipe
#         fields = ['ingredient', 'amount', 'unit']
    
#     def clean_ingredient(self):
#         ingredient_name = self.cleaned_data.get('ingredient')
#         try:
#             ingredient = Ingredient.objects.get(name=ingredient_name)
#         except Ingredient.DoesNotExist:
#             raise ValidationError("Selected ingredient does not exist.")
#         return ingredient
    

IngredientPerRecipeFormSet = inlineformset_factory(
    Recipe,
    IngredientPerRecipe,
    fields = ['ingredient', 'amount', 'unit'],
    extra=1,
    can_delete=True,
    widgets = {
        "id": HiddenInput(attrs={"class": "id-input"}),
        "ingredient": HiddenInput(attrs={"required": "required", "class": "form-control search-box-id"}),
        "amount": NumberInput(attrs={"required": "required", "class": "form-control amount-input"}),
        "unit": Select(attrs={"required": "required", "class": "form-control form-select unit-input"}),
    },
)


