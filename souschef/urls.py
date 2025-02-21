from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home_search/", views.home_search, name="home_search"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("recipes", views.recipes, name="recipes"),
    path("recipe/<int:id>", views.recipe, name="recipe"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("update_recipe_image/", views.update_recipe_image, name="update_recipe_image"),
    path("delete_recipe/<int:id>", views.delete_recipe, name="delete_recipe"),
    path("pantry/", views.pantry, name="pantry"),
    path("pantry_delete/", views.pantry_delete, name="pantry_delete"),
    path("ingredient_details/", views.ingredient_details, name="ingredient_details"),
    path("ingredient/<int:id>", views.ingredient, name="ingredient"),
    path("favourite/<int:id>", views.favourite, name="favourite"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)