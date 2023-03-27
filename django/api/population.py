"""
Usage and Examples

Start the Django shell by `./manage.py shell`

In [1]: from api.population import populate

In [2]: populate(range(100, 103))
Created a user 'user100' with 34 ingredients and 29 recipes
Created a user 'user101' with 26 ingredients and 11 recipes
Created a user 'user102' with 35 ingredients and 15 recipes

In [3]: populate(range(103, 105), th_cooked=0.2, nr=30, ni=20)
Created a user 'user103' with 20 ingredients and 30 recipes
Created a user 'user104' with 20 ingredients and 30 recipes

"""

import random
from datetime import datetime, timedelta

import pytz

from django.db.models import Count

from .models import (
    Ingredient,
    QuantityScaleUnit,
    Recipe,
    RecipeIngredient,
    StorageLocation,
    User,
    UserIngredient,
    UserRecipeFavorite,
    UserRecipeHistory,
)


def randomIngredient():
    return Ingredient.objects.order_by("?").first()


def randomRecipe():
    return Recipe.objects.order_by("?").first()


def generateUserIngredient(user: User, ingredient: Ingredient, **kwargs):
    if UserIngredient.objects.filter(user=user, ingredient=ingredient):
        # avoid duplication
        return None

    consumed = random.random() > float(kwargs.get("th_consumed", 0.5))
    qval = random.randint(1, 3)
    qscale = QuantityScaleUnit.objects.get(
        id=(
            RecipeIngredient.objects.filter(ingredient=ingredient)
            .values("quantity_scale")
            .annotate(c=Count("quantity_scale"))
            .order_by("-c")
            .first()
        )["quantity_scale"]
    )

    if ingredient.freezer_days:
        storage = StorageLocation.FREEZER
        expiration = ingredient.freezer_days
    elif ingredient.refrigerator_days:
        storage = StorageLocation.REFRIGERATOR
        expiration = ingredient.refrigerator_days
    else:
        storage = StorageLocation.PANTRY
        expiration = ingredient.pantry_days or 2 * 365
    expiration_date = datetime.now(pytz.timezone("UTC")) + timedelta(days=expiration)

    happiness = random.randint(0, 100)
    ui = UserIngredient(
        user=user,
        ingredient=ingredient,
        quantity_value=qval,
        quantity_scale=qscale,
        consumed=consumed,
        storage=storage,
        expiration_date=expiration_date.isoformat(),
        happiness=happiness,
    )
    ui.save()
    return ui


def generateUserRecipe(user: User, recipe: Recipe, **kwargs):
    if UserRecipeHistory.objects.filter(user=user, recipe=recipe):
        # avoid duplication
        return None, None

    cooked = random.random() > float(kwargs.get("th_cooked", 0.5))
    access_date = datetime.now(pytz.timezone("UTC")) - timedelta(
        days=random.randint(0, 200)
    )
    urh = UserRecipeHistory(user=user, recipe=recipe, cooked=cooked)
    urh.save()
    urh.access_date = access_date.isoformat()  # somehow could not do at once
    urh.save()
    if random.random() > float(kwargs.get("th_fav", 0.5)):
        added_date = min(
            access_date + timedelta(days=random.randint(0, 10)),
            datetime.now(pytz.timezone("UTC")),
        )
        urf = UserRecipeFavorite(user=user, recipe=recipe)
        urf.save()
        urf.added_date = added_date.isoformat()  # somehow could not do at once
        urf.save()
        return urh, urf
    return urh, None


def generateUser(username, **kwargs):
    if User.objects.filter(username=username):
        # avoid duplication
        print(f"a user with username {repr(username)} already exists")
        return None

    verbose = bool(kwargs.get("v")) or bool(kwargs.get("verbose"))

    password = kwargs.get("password", "testpass")
    u = User.objects.create_user(username=username, password=password)
    if verbose:
        print("Created a new user:", u)

    default_ni = random.randint(10, 40)
    ni = int(kwargs.get("ni", default_ni))  # num user-ingredients
    for _ in range(ni):
        i = randomIngredient()
        ui = generateUserIngredient(u, i, **kwargs)
        if verbose:
            print("\t", ui)

    default_nr = random.randint(10, 40)
    nr = int(kwargs.get("nr", default_nr))  # num user-recipes
    for _ in range(nr):
        r = randomRecipe()
        urh, urf = generateUserRecipe(u, r, **kwargs)
        if verbose:
            print("\t", "Fav" if urf else "   ", urh)

    print(f"Created a user {repr(username)} with {ni} ingredients and {nr} recipes")
    return u


def populate(_num_range, **kwargs):
    for v in _num_range:
        username = f"user{v}"
        generateUser(username, **kwargs)
