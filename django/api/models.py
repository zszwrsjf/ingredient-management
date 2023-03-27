from api.querysets import IngredientQuerySet, RecipeQuerySet

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.utils import IntegrityError

# Create your models here.


# language is in order of population
class LanguageOption(models.TextChoices):
    EN = "en", "english"
    ES = "es", "spanish"
    ZH = "zh", "chinese"
    DE = "de", "german"
    JA = "ja", "japanese"
    KO = "ko", "korean"
    HE = "he", "hebrew"


# ingredient storage choices
class StorageLocation(models.IntegerChoices):
    PANTRY = 0, "pantry"
    REFRIGERATOR = 1, "refrigerator"
    FREEZER = 2, "freezer"


User = get_user_model()


class Ingredient(models.Model):
    objects = IngredientQuerySet.as_manager()

    name = models.CharField(unique=True, max_length=128)
    info_url = models.URLField(null=True, blank=True, max_length=1024)
    image_url = models.URLField(null=True, blank=True, max_length=1024)
    category = models.CharField(null=True, blank=True, max_length=128, default="foods")
    pantry_days = models.PositiveIntegerField(null=True, blank=True)
    refrigerator_days = models.PositiveIntegerField(null=True, blank=True)
    freezer_days = models.PositiveIntegerField(null=True, blank=True)
    owners = models.ManyToManyField(
        User, through="UserIngredient", related_name="ingredients"
    )

    def __str__(self):
        return self.name

    def save_or_update_min(self):
        """Returns True if updated an existing record"""

        try:
            self.save()
            return False
        except IntegrityError:
            found = Ingredient.objects.filter(name=self.name).first()
            updated = False
            if self.pantry_days is not None and (
                found.pantry_days is None or self.pantry_days < found.pantry_days
            ):
                found.pantry_days = self.pantry_days
                updated = True
            if self.refrigerator_days is not None and (
                found.refrigerator_days is None
                or self.refrigerator_days < found.refrigerator_days
            ):
                found.refrigerator_days = self.refrigerator_days
                updated = True
            if self.freezer_days is not None and (
                found.freezer_days is None or self.freezer_days < found.freezer_days
            ):
                found.freezer_days = self.freezer_days
                updated = True
            if updated:
                found.info_url = self.info_url
                found.save()
            return updated


class Recipe(models.Model):
    objects = RecipeQuerySet.as_manager()

    title = models.CharField(max_length=64)
    recipe_url = models.URLField(blank=True, max_length=1024)
    image_url = models.URLField(blank=True, max_length=2048)
    cook_minute = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )
    num_servings = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(
        default=LanguageOption.EN, max_length=2, choices=LanguageOption.choices
    )
    num_ingredients = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of types of ingredients, for sanity check purpose",
    )

    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", related_name="recipes"
    )
    users_who_viewed = models.ManyToManyField(
        User, through="UserRecipeHistory", related_name="viewed_recipes"
    )
    users_who_liked = models.ManyToManyField(
        User, through="UserRecipeFavorite", related_name="liked_recipes"
    )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "recipe_url"],
                name="unique_recipe_title_url",
            )
        ]


class Tag(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128, default="default")
    description = models.CharField(blank=True, max_length=128)
    info_url = models.URLField(blank=True, max_length=2048)
    image_url = models.URLField(blank=True, max_length=2048)
    language = models.CharField(
        default=LanguageOption.EN, max_length=2, choices=LanguageOption.choices
    )

    recipes = models.ManyToManyField(Recipe, through="RecipeTag", related_name="tags")

    def __str__(self):
        return f"{self.category}::{self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="unique_name_category",
            )
        ]


class QuantityScaleUnit(models.Model):
    unit = models.CharField(unique=True, max_length=16)
    description = models.CharField(null=True, blank=True, max_length=256)


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_value = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    quantity_scale = models.ForeignKey(
        QuantityScaleUnit, null=True, on_delete=models.PROTECT
    )
    consumed = models.BooleanField(default=False)
    storage = models.IntegerField(
        default=StorageLocation.REFRIGERATOR, choices=StorageLocation.choices
    )
    created_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    happiness = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )

    def __str__(self):
        return f"user: {str(self.user)}, ingredient: {str(self.ingredient)}"

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            return  # just return if already saved
        except ValueError:  # one of the foreign keys are not saved
            try:
                self.quantity_scale.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.quantity_scale = QuantityScaleUnit.objects.filter(
                    unit=self.quantity_scale.unit
                ).first()

            try:
                super().save(*args, **kwargs)
            except IntegrityError:
                return  # just return if already saved


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_value = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    quantity_scale = models.ForeignKey(
        QuantityScaleUnit, null=True, on_delete=models.PROTECT
    )
    weight = models.DecimalField(null=True, decimal_places=2, max_digits=7)  # in grams

    def __str__(self):
        return f"recipe: {str(self.recipe)}, ingredient: {str(self.ingredient)}"

    def save(self, *args, **kwargs):
        """Wrapper that, if necessary, saves foreign keys to avoid ValueError"""

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            return  # just return if already saved
        except ValueError:  # one of the foreign keys are not saved
            try:
                self.recipe.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.recipe = Recipe.objects.filter(title=self.recipe.title).first()

            try:
                self.ingredient.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.ingredient = Ingredient.objects.filter(
                    name=self.ingredient.name
                ).first()

            try:
                self.quantity_scale.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.quantity_scale = QuantityScaleUnit.objects.filter(
                    unit=self.quantity_scale.unit
                ).first()

            try:
                super().save(*args, **kwargs)
            except IntegrityError:
                return  # just return if already saved

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"recipe: {str(self.recipe)}, tag: {str(self.tag)}"

    def save(self, *args, **kwargs):
        """Wrapper that, if necessary, saves foreign keys to avoid ValueError"""

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            return  # just return if already saved
        except ValueError:  # one of the foreign keys are not saved
            try:
                self.recipe.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.recipe = Recipe.objects.filter(title=self.recipe.title).first()

            try:
                self.tag.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.tag = Tag.objects.filter(name=self.tag.name).first()

            try:
                super().save(*args, **kwargs)
            except IntegrityError:
                return  # just return if already saved

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "tag"],
                name="unique_recipe_tag",
            )
        ]


class RecipeNutrition(models.Model):
    recipe = models.OneToOneField(
        Recipe, on_delete=models.CASCADE, primary_key=True, related_name="nutrition"
    )
    calories_kcal_per_serving = models.FloatField(
        validators=[MinValueValidator(0.0)], default=0
    )
    fat_gram_per_serving = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )
    carbs_gram_per_serving = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )
    protein_gram_per_serving = models.FloatField(
        validators=[MinValueValidator(0.0)], null=True, blank=True
    )

    def __str__(self):
        return ", ".join(
            [
                f"Recipe: {self.recipe.title}",
                f"Energy: {self.calories_kcal_per_serving} kCal",
                f"Protein: {self.protein_gram_per_serving} g",
                f"Fat: {self.fat_gram_per_serving} g",
                f"Carb: {self.carbs_gram_per_serving} g",
            ]
        )

    def save(self, *args, **kwargs):
        """Wrapper that saves 'recipe', if necessary, to avoid ValueError"""

        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            return  # just return if already saved
        except ValueError:  # one of the foreign keys are not saved
            try:
                self.recipe.save()
            except IntegrityError:  # uniqueness error, so update our ref
                self.recipe = Recipe.objects.filter(title=self.recipe.title).first()

            try:
                super().save(*args, **kwargs)
            except IntegrityError:
                return  # just return if already saved


class UserRecipeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    cooked = models.BooleanField(default=False)

    def __str__(self):
        return f"user: {str(self.user)}, recipe: {str(self.recipe)}"


class UserRecipeFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {str(self.user)}, recipe: {str(self.recipe)}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe",
            )
        ]
