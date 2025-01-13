from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path("recipes", views.recipes, name="recipes"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("pantry/", views.pantry, name="pantry"),
    path("ingredient_details/", views.ingredient_details, name="ingredient_details"),
    path("recipe_ingredient/", views.recipe_ingredient, name="recipe_ingredient"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]