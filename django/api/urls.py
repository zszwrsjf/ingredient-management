from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import path

from . import views

urlpatterns = [
    # recipes/
    path("recipes/search", views.SearchRecipe.as_view()),
    path("recipes/statistics", views.RecipesStatistics.as_view()),
    path("recipes/random", views.RecipesRandom.as_view()),
    # ingredients/
    path("ingredients", views.Ingredients.as_view()),
    path("ingredients/search", views.SearchIngredient.as_view()),
    path("ingredients/statistics", views.IngredientsStatistics.as_view()),
    # units/
    path("units", views.Units.as_view({"get": "list", "post": "create"})),
    path("units/<int:pk>", views.Units.as_view({"get": "retrieve", "put": "update"})),
    # user/
    path("user/ingredients", views.UsersIngredients.as_view()),
    path("user/recipes", views.UsersRecipesHistory.as_view()),
    path("user/favorite", views.UsersFavoriteRecipes.as_view()),
    path("user/stats", views.UsersStatistics.as_view()),
    # token/
    path("token", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("signup", views.SignupView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
