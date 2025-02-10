from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, ModelChoiceField, IntegerField, HiddenInput, ClearableFileInput

from .models import Ingredient, Recipe, PantryIngredient, IngredientPerRecipe, Step, UserDashboard

from django.forms import inlineformset_factory


class UserDashboardForm(ModelForm):
    class Meta:
        model = UserDashboard
        fields = ["profile_picture"]
        widgets = {
            "profile_picture": ClearableFileInput(attrs={"rows": 1, "class": "form-control profile_form", "id": "pictureUpload", "type": "file"}),
        }


class NewRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "image"]
        widgets = {
            "title": Textarea(attrs={"rows": 1, "class": "form-control custom-input"}),
            "description": Textarea(attrs={"cols": 40, "rows": 5, "class": "form-control custom-input"}),
            "image": ClearableFileInput(attrs={"rows": 1, "class": "form-control", "id": "imageUpload", "type": "file"}),
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


### Receipe Steps Formset
StepFormSet = inlineformset_factory(
    Recipe,
    Step,
    can_delete=True,
    fields=('step_number', 'step_text'),
    widgets = {
        "id": HiddenInput(attrs={"class": "step-id-input"}),
        "step_number": HiddenInput(attrs={"class": "step-number-input"}),
        "step_text": TextInput(attrs={"required": "required", "class": "form-control step-text-input", "placeholder": "Step", "aria-label": "Step", "aria-describedby": "button-addon2"}),
    },
)    


### Recipe Ingredients Formset
IngredientPerRecipeFormSet = inlineformset_factory(
    Recipe,
    IngredientPerRecipe,
    can_delete=True,
    fields = ['ingredient', 'amount', 'unit'],
    widgets = {
        "id": HiddenInput(attrs={"class": "id-input"}),
        "ingredient": HiddenInput(attrs={"required": "required", "class": "form-control search-box-id"}),
        "amount": NumberInput(attrs={"required": "required", "class": "form-control amount-input"}),
        "unit": Select(attrs={"required": "required", "class": "form-control form-select unit-input"}),
    },
)


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