from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class UserDashboard(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_name")
    created = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to="static/images/profile_pics", null=True, blank=True)
    favourites = models.ManyToManyField('Recipe', blank=True, related_name='favourite_of')

    def __str__(self):
        return f"{self.user_name}"
    
    
class Pantry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user_name}'s Pantry"
    
    
class Unit(models.Model):
    unit_type = models.CharField(max_length=8)

    def __str__(self):
        return self.unit_type
    

class Ingredient(models.Model):
    name = models.CharField(max_length=64, blank=False)
    ingredient_id = models.IntegerField(unique=True)
    # category = models.ForeignKey(FoodType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
    

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through="IngredientPerRecipe")
    image = models.ImageField(upload_to="static/images/recipe_pics", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}, ID:{self.id}"
    

class IngredientPerRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ingredient: {self.ingredient}"
    
    
class PantryIngredient(models.Model):
    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    step_text = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.step_number}"
    

# class FoodType(models.Model):
#     category = models.CharField(max_length=64)

#     def __str__(self):
#         return self.category