from django.contrib import admin
from .models import User, UserDashboard, FoodType, Unit, Ingredient, Pantry, PantryIngredient

admin.site.register(User)
admin.site.register(UserDashboard)
admin.site.register(FoodType)
admin.site.register(Unit)

class PantryIngredientInline(admin.TabularInline):
    model = PantryIngredient
    extra = 1
    fields = ['ingredient', 'quantity', 'unit']


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    list_display = ('pantry_name',)
    inlines = [PantryIngredientInline]

    def pantry_name(self, obj):
        return str(obj)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
