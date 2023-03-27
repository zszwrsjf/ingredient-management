import random
from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import (
    BooleanField,
    Count,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    Value,
)
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import (
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
from .serializers import (
    CustomTokenObtainPairSerializer,
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        """
        Register a new user to DB
        """
        try:
            serializer = UserSerializer(
                data={
                    "username": request.data["username"],
                    "email": request.data["email"],
                    "password": request.data["password"],
                }
            )
        except KeyError:
            raise ParseError()

        if serializer.is_valid(raise_exception=True):
            res = serializer.save()
            return Response({"user_id": res.id}, status=status.HTTP_201_CREATED)


class UsersIngredients(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Get list of active user-ingredients (not consumed) of a user.
        """
        user_id = request.auth["user_id"] if request.auth else None
        uis = UserIngredient.objects.filter(
            consumed=False, user=user_id
        ).prefetch_related(
            Prefetch("ingredient", queryset=Ingredient.objects.annotate_all(user_id))
        )

        return Response(
            UserIngredientSerializer(uis, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        """
        Add a new ingredient for a user.
        """
        try:
            res = UserIngredient.objects.create(
                user=User.objects.get(id=request.auth["user_id"]),
                ingredient=Ingredient.objects.get(id=request.data["ingredient_id"]),
                quantity_value=request.data["quantity_value"],
                quantity_scale=QuantityScaleUnit.objects.get(
                    id=request.data["quantity_scale_unit_id"]
                ),
                storage=request.data["storage"],
                expiration_date=datetime.fromisoformat(
                    request.data["expiration_date"].replace("Z", "+00:00")
                ),
                happiness=request.data["happiness"],
            )
            return Response(
                {
                    **UserIngredientSerializer(res).data,
                    "ingredient": res.ingredient.id,  # overwrite
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Edit an ingredient for a user only if such ingredient exists.
        """
        try:
            data = request.data
            user_ingredient = UserIngredient.objects.get(id=data["user_ingredient_id"])
            user_ingredient.user = User.objects.get(id=request.auth["user_id"])
            for key in ["quantity_value", "consumed", "storage", "happiness"]:
                if key in data:
                    setattr(user_ingredient, key, data[key])
            if "ingredient_id" in data:
                user_ingredient.ingredient = Ingredient.objects.get(
                    id=data["ingredient_id"]
                )
            if "quantity_scale_unit_id" in data:
                user_ingredient.quantity_scale = QuantityScaleUnit.objects.get(
                    id=data["quantity_scale_unit_id"]
                )
            if "expiration_date" in data:
                user_ingredient.expiration_date = datetime.fromisoformat(
                    data["expiration_date"].replace("Z", "+00:00")
                )
            user_ingredient.save()
            return Response(
                {
                    **UserIngredientSerializer(user_ingredient).data,
                    "ingredient": user_ingredient.ingredient.id,  # overwrite
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Ingredients(APIView):
    def get(self, request, format=None):
        try:
            user_id = request.auth["user_id"] if request.auth else None
            ings = request.query_params.getlist("ingredient")
            res = Ingredient.objects.filter(id__in=ings).annotate_all(user_id)
            return Response(
                IngredientSerializer(res, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class SearchIngredient(APIView):
    def get(self, request, format=None):
        """
        Get a list of ingredients matched with the search criteria.
        """
        user_id = request.auth["user_id"] if request.auth else None
        allowed_queries = {"icontains"}
        if set(request.query_params).difference(allowed_queries):
            return Response(
                [], status=status.HTTP_400_BAD_REQUEST
            )  # contains invalid queries

        ings = Ingredient.objects.annotate_all(user_id).filter(
            name__icontains=request.query_params.get("icontains", "")
        )
        return Response(
            IngredientSerializer(ings, many=True).data,
            status=status.HTTP_200_OK,
        )


class SearchRecipe(APIView):
    def get(self, request, format=None):
        """
        Get recipes search results based on search criterias.
        """
        user_id = request.auth["user_id"] if request.auth else None
        ingredient_list = request.query_params.getlist("ingredient")
        mode_selection = request.query_params.get("mode").lower()
        strict_filter = request.query_params.get("strict").lower() == "true"

        res = Recipe.objects
        try:
            res = res.annotate(c=Count("ingredients", distinct=True))
            if strict_filter:
                res = res.filter(num_ingredients=F("c"))
            if len(ingredient_list) > 0:
                if mode_selection == "exact":
                    if strict_filter:
                        res = res.filter(c=len(ingredient_list))
                    for ing in ingredient_list:
                        res = res.filter(ingredients=ing)
                elif mode_selection == "any":
                    res = res.filter(ingredients__in=ingredient_list)
                    if strict_filter:
                        exc_items = Ingredient.objects.exclude(id__in=ingredient_list)
                        res = res.exclude(ingredients__in=exc_items)
            res = res.annotate(
                bm=Count(
                    "ingredients",
                    filter=Q(ingredients__id__in=ingredient_list),
                    distinct=True,
                )
            ).order_by("-bm")
            res = res.annotate_all(user_id).distinct()[:30]

            return Response(
                RecipeSerializer(res, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UsersRecipesHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Get recipe history information of user.
        """
        user_id = request.auth["user_id"] if request.auth else None
        urhs = (
            UserRecipeHistory.objects.filter(user=user_id)
            .prefetch_related(
                Prefetch("recipe", queryset=Recipe.objects.annotate_all(user_id))
            )
            .order_by("-access_date")
            .annotate(
                favorite=Exists(
                    UserRecipeFavorite.objects.filter(
                        user=OuterRef("user"), recipe=OuterRef("recipe")
                    )
                )
            )
        )

        return Response(
            UserRecipeHistorySerializer(urhs, many=True, read_only=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        """
        Add recipe history information of user.
        """
        try:
            data = request.data
            if (
                UserRecipeHistory.objects.filter(
                    user=request.auth["user_id"], recipe=data["recipe_id"]
                ).count()
                > 0
            ):
                return self.put(request=request, format=format)
            res = UserRecipeHistory.objects.create(
                user=User.objects.get(id=request.auth["user_id"]),
                recipe=Recipe.objects.get(id=data["recipe_id"]),
                access_date=timezone.now(),
                cooked=data["cooked"] if "cooked" in data else False,
            )
            return Response(
                {
                    **UserRecipeHistorySerializer(res).data,
                    "recipe": res.recipe.id,  # overwrite
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        Update user recipe history item
        """
        try:
            user_id = request.auth["user_id"]
            data = request.data
            res = UserRecipeHistory.objects.get(user=user_id, recipe=data["recipe_id"])
            res.cooked = data["cooked"] if "cooked" in data else False
            res.access_date = timezone.now()
            res.save()
            return Response(
                {
                    **UserRecipeHistorySerializer(res).data,
                    "recipe": res.recipe.id,  # overwrite
                },
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            return self.post(request=request, format=format)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Delete recipe information of user.
        """
        try:
            data = request.data
            res = UserRecipeHistory.objects.get(id=data["user_recipe_history_id"])
            n, _ = res.delete()
            return Response(
                {
                    "message": "Delete successful.",
                    "deleted": n,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UsersFavoriteRecipes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Get favorite recipe information of user.
        """
        user_id = request.auth["user_id"] if request.auth else None
        urfs = (
            UserRecipeFavorite.objects.filter(user=user_id)
            .prefetch_related(
                Prefetch("recipe", queryset=Recipe.objects.annotate_all(user_id))
            )
            .order_by("-added_date")
        )

        return Response(
            UserRecipeFavoriteSerializer(urfs, many=True, read_only=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        """
        Add recipe information of user.
        """
        try:
            data = request.data
            res = UserRecipeFavorite.objects.create(
                user=User.objects.get(id=request.auth["user_id"]),
                recipe=Recipe.objects.get(id=data["recipe_id"]),
                added_date=timezone.now(),
            )
            return Response(
                {
                    **UserRecipeFavoriteSerializer(res).data,
                    "recipe": res.recipe.id,  # overwrite
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """
        Remove recipe from user favorites.
        """
        try:
            recipe_id = request.data["recipe_id"]
            res = UserRecipeFavorite.objects.get(
                user=request.auth["user_id"], recipe=recipe_id
            )
            n, _ = res.delete()
            return Response(
                {
                    "message": "Delete successful.",
                    "deleted": n,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UsersStatistics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_id = request.auth["user_id"] if request.auth else None
            return Response(
                {
                    "user": user_id,
                    "all_cooked": UserRecipeHistory.objects.filter(
                        user=user_id, cooked=True
                    )
                    .distinct()
                    .count(),
                    "all_liked": UserRecipeFavorite.objects.filter(
                        user=user_id
                    ).count(),
                    "all_ingredients": UserIngredient.objects.filter(
                        user=user_id, consumed=False
                    )
                    .distinct()
                    .count(),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class Units(ModelViewSet):
    queryset = QuantityScaleUnit.objects.all()
    serializer_class = QuantityScaleUnitSerializer

    def list(self, request, *args, **kwargs):
        ingredient_id = request.query_params.get("ingredient_id")
        try:
            units = QuantityScaleUnit.objects
            if ingredient_id:
                units = units.annotate(
                    c=Count(
                        "recipeingredient",
                        filter=Q(recipeingredient__ingredient=ingredient_id),
                    )
                )
            else:
                units = units.annotate(
                    c=Count(
                        "recipeingredient",
                    )
                )
            # based on: https://www.adducation.info/how-to-improve-your-knowledge/units-of-measurement/
            units = (
                units.order_by("-c")
                .filter(c__gt=0)
                .filter(
                    unit__in=[
                        "gram",
                        "kilogram",
                        "ounce",
                        "pound",
                        "liter",
                        "milliliter",
                        "pint",
                        "quart",
                        "gallon",
                    ]
                )
            )
            if units.count() <= 0:
                units = QuantityScaleUnit.objects.filter(unit="unit")
            return Response(
                QuantityScaleUnitSerializer(units, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class RecipesStatistics(APIView):
    def get(self, request, format=None):
        """
        Returns statistics about recipes (10 most cooked, 10 most liked, 10 most viewed).
        """
        pass


class RecipesRandom(APIView):
    def get(self, request, format=None):
        """
        Returns a random recipe from the database.
        """
        user_id = request.auth["user_id"] if request.auth else None
        rec = Recipe.objects.annotate_all(user_id).all()
        count = Recipe.objects.count()
        random_number = random.randint(0, count - 1)
        return Response(
            RecipeSerializer(rec[random_number]).data,
            status=status.HTTP_200_OK,
        )


class IngredientsStatistics(APIView):
    def get(self, request, format=None):
        """
        Returns statistics about ingredients (10 most used, 10 most happy).
        """
        pass
