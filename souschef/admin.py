from django.contrib import admin
from .models import User, UserDashboard, Unit, Ingredient, Pantry, PantryIngredient, Recipe, Step, IngredientPerRecipe

admin.site.register(User)
admin.site.register(UserDashboard)
admin.site.register(Unit)


class PantryIngredientInline(admin.TabularInline):
    model = PantryIngredient
    extra = 1
    fields = ['name', 'quantity', 'unit']


class IngredientPerRecipeInline(admin.TabularInline):
    model = IngredientPerRecipe
    extra = 1
    fields = ['ingredient', 'amount', 'unit']


class StepInline(admin.TabularInline):
    model = Step
    extra = 0
    fields = ['step_number', 'step_text']


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    list_display = ('pantry_name',)
    inlines = [PantryIngredientInline]

    def pantry_name(self, obj):
        return str(obj)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredient_id')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [IngredientPerRecipeInline, StepInline]
