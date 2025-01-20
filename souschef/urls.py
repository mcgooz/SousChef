from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home_search/", views.home_search, name="home_search"),
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path("recipes", views.recipes, name="recipes"),
    path("recipe/<int:id>", views.recipe, name="recipe"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("pantry/", views.pantry, name="pantry"),
    path("ingredient_details/", views.ingredient_details, name="ingredient_details"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path("recipe_ingredient/", views.recipe_ingredient, name="recipe_ingredient"),