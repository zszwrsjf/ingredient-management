from django.db import models
from django.db.models import Case, Count, Exists, F, OuterRef, Prefetch, Q, When


class IngredientQuerySet(models.QuerySet):
    def annotate_all(self, user=None):
        ret = self
        if user:
            ret = ret.annotate_user(user)
        return ret

    def annotate_user(self, user):
        """annotate user-related fields"""
        return self.annotate(
            in_storage=Exists(
                self.filter(
                    Q(useringredient__ingredient=OuterRef("pk"))
                    & Q(useringredient__user=user)
                    & Q(useringredient__consumed=False)
                )
            ),
        )


class RecipeQuerySet(models.QuerySet):
    def annotate_all(self, user=None):
        from .models import Ingredient  # local import to avoid circular imports

        ret = (
            self.select_related("nutrition")
            .prefetch_related(
                Prefetch(
                    "recipeingredient_set__ingredient",
                    queryset=Ingredient.objects.annotate_all(user),
                ),
                "tags",
            )
            .annotate_stats()
        )
        if user:
            ret = ret.annotate_user(user)
        return ret

    def annotate_stats(self):
        """annotate statistics"""
        return self.annotate(
            all_cooked=Count(
                "userrecipehistory",
                filter=Q(userrecipehistory__cooked=True),
                distinct=True,
            ),
            all_favorite=Count("userrecipefavorite", distinct=True),
        )

    def annotate_user(self, user):
        """annotate user-related fields"""
        return self.annotate(
            user_cooked=Exists(
                self.filter(
                    Q(userrecipehistory__recipe=OuterRef("pk"))
                    & Q(userrecipehistory__cooked=True)
                    & Q(userrecipehistory__user=user)
                )
            ),
            user_favorite=Exists(
                self.filter(
                    Q(userrecipefavorite__recipe=OuterRef("pk"))
                    & Q(userrecipefavorite__user=user)
                )
            ),
        )
