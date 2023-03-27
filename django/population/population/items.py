# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from api.models import (
    Ingredient,
    QuantityScaleUnit,
    Recipe,
    RecipeIngredient,
    RecipeNutrition,
    RecipeTag,
    Tag,
)
from scrapy_djangoitem import DjangoItem


class IngredientItem(DjangoItem):
    django_model = Ingredient


class RecipeItem(DjangoItem):
    django_model = Recipe


class TagItem(DjangoItem):
    django_model = Tag


class QuantityScaleUnitItem(DjangoItem):
    django_model = QuantityScaleUnit


class RecipeIngredientItem(DjangoItem):
    django_model = RecipeIngredient


class RecipeTagItem(DjangoItem):
    django_model = RecipeTag


class RecipeNutritionItem(DjangoItem):
    django_model = RecipeNutrition
