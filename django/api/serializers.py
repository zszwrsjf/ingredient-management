from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        return User.objects.create_user(
            username=username, email=email, password=password
        )


class IngredientSerializer(serializers.ModelSerializer):
    # annotated fields
    in_storage = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Ingredient
        exclude = ["owners"]


class RecipeNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNutrition
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["recipes"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    # override relational fields
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = "__all__"


class QuantityScaleUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityScaleUnit
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    # override relational fields
    nutrition = RecipeNutritionSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True, many=True, source="recipeingredient_set"
    )

    # annotated fields
    user_cooked = serializers.BooleanField(read_only=True, default=False)
    user_favorite = serializers.BooleanField(read_only=True, default=False)
    all_cooked = serializers.IntegerField(read_only=True)
    all_favorite = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ["users_who_viewed", "users_who_liked"]


class UserRecipeFavoriteSerializer(serializers.ModelSerializer):
    # override relational fields
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = UserRecipeFavorite
        fields = "__all__"


class UserRecipeHistorySerializer(serializers.ModelSerializer):
    # override relational fields
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = UserRecipeHistory
        fields = "__all__"


class UserIngredientSerializer(serializers.ModelSerializer):
    # override relational fields
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = UserIngredient
        fields = "__all__"
