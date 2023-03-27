import json
from itertools import chain

from api.models import (
    Ingredient,
    QuantityScaleUnit,
    Recipe,
    RecipeIngredient,
    RecipeNutrition,
    RecipeTag,
    Tag,
    User,
    UserIngredient,
    UserRecipeFavorite,
    UserRecipeHistory,
)
from api.serializers import (
    IngredientSerializer,
    QuantityScaleUnitSerializer,
    RecipeIngredientSerializer,
    RecipeNutritionSerializer,
    RecipeSerializer,
    RecipeTagSerializer,
    TagSerializer,
    UserIngredientSerializer,
    UserRecipeFavoriteSerializer,
    UserRecipeHistorySerializer,
    UserSerializer,
)
from rest_framework.serializers import ModelSerializer

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

TARGETS = [
    ("ingredient", Ingredient, IngredientSerializer),
    ("recipe", Recipe, RecipeSerializer),
    ("tag", Tag, TagSerializer),
    ("recipe-ingredient", RecipeIngredient, RecipeIngredientSerializer),
    ("recipe-tag", RecipeTag, RecipeTagSerializer),
    ("nutrition", RecipeNutrition, RecipeNutritionSerializer),
    ("users", User, UserSerializer),
    ("user-ingredient", UserIngredient, UserIngredientSerializer),
    ("user-recipe-favorite", UserRecipeFavorite, UserRecipeFavoriteSerializer),
    ("user-recipe-history", UserRecipeHistory, UserRecipeHistorySerializer),
    ("units", QuantityScaleUnit, QuantityScaleUnitSerializer),
]


def _get_records(model: Model, serializer: ModelSerializer):
    return list(
        map(
            lambda ins: _to_dict(
                ins, exclude=getattr(serializer.Meta, "exclude", None)
            ),
            model.objects.all(),
        )
    )


def _to_dict(instance, fields=None, exclude=None):
    """
    Returns dict from the given instance similarly to `model_to_dict`,
    but this function also returns non-editable fields unlike it.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, "editable", False):
            pass  # DO NOT SKIP unlike `model_to_dict`!
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def export(path=".db.json", indent=None, override=True):
    data = {}

    for name, model, serializer in TARGETS:
        data[name] = _get_records(model, serializer)

    mode = "w" if override else "x"  # exclusive creation

    with open(path, mode) as f:
        json.dump(data, f, cls=DjangoJSONEncoder, indent=indent)
