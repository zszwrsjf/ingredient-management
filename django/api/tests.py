from datetime import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from .models import (Ingredient, QuantityScaleUnit, Recipe, RecipeIngredient,
                     RecipeNutrition, User, UserIngredient, UserRecipeFavorite,
                     UserRecipeHistory)


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.urls = ["/api/user/ingredients", "/api/user/recipes", "/api/user/favorite"]
        self.public_urls = [  # excluding lib-managed token endpoints
            "/api/recipes/search?mode=exact&strict=true",
            "/api/ingredients/search",
            "/api/units",
        ]

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def verifyGETStatus(self, urls, expected_status):
        """helper method for testing GET"""
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, expected_status)

    def test_public_urls_are_always_accessible(self):
        """
        should be accessible with and without tokens
        """
        self.verifyGETStatus(self.public_urls, 200)

        u = User.objects.create_user(username="user1", password="testpass")
        self.setupToken(u.username)

        self.verifyGETStatus(self.public_urls, 200)

    def test_with_an_valid_token(self):
        """
        should return 200 for requests with an valid token
        """
        u = User.objects.create_user(username="user1", password="testpass")
        self.setupToken(u.username)

        self.verifyGETStatus(self.urls, 200)

    def test_without_auth_header(self):
        """
        should return 401 for requests without auth header
        """

        self.verifyGETStatus(self.urls, 401)

    def test_with_empty_token(self):
        """
        should return 401 for requests with an empty token
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer ")

        self.verifyGETStatus(self.urls, 401)

    def test_with_an_invalid_token(self):
        """
        should return 401 for requests with an invalid token
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer j.w.t")

        self.verifyGETStatus(self.urls, 401)


class SignupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_success(self):
        """should receive the ID of the created user on success"""
        username, email, password = "user1", "user1@users.com", "testpass"
        res = self.client.post(
            "/api/signup",
            {"username": username, "email": email, "password": password},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue("user_id" in res.json())
        self.assertEqual(res.json()["user_id"], User.objects.first().id)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, username)

    def test_missing_property(self):
        """should receive 400"""
        res = self.client.post("/api/signup", {"username": "user1"}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertTrue("detail" in res.json())
        self.assertTrue("Malformed" in res.json()["detail"])

    def test_unexpected_property(self):
        """should receive 400"""
        res = self.client.post(
            "/api/signup", {"name": "myname", "pass": "word"}, format="json"
        )
        self.assertEqual(res.status_code, 400)
        self.assertTrue("detail" in res.json())
        self.assertTrue("Malformed" in res.json()["detail"])

    def test_dup_username(self):
        """should receive 400"""
        username, email, password = "user1", "user1@users.com", "testpass"
        User.objects.create_user(username=username, password=password)
        res = self.client.post(
            "/api/signup",
            {"username": username, "email": email, "password": password},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertTrue("username" in res.json())
        self.assertEqual(len(res.json()["username"]), 1)
        self.assertTrue("already exists" in res.json()["username"][0])

    def test_empty_password(self):
        """should receive 400"""
        res = self.client.post(
            "/api/signup",
            {"username": "user1", "email": "user1@users.com", "password": ""},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertTrue("password" in res.json())
        self.assertEqual(len(res.json()["password"]), 1)
        self.assertEqual(res.json()["password"][0], "This field may not be blank.")


class SearchIngredientTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_with_correct_param(self):
        """GET with correct parameter"""
        i1 = Ingredient.objects.create(name="carrot")
        Ingredient.objects.create(name="onion")

        res = self.client.get("/api/ingredients/search?icontains=ARr")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["id"], i1.id)

    def test_get_with_incorrect_param(self):
        """GET with incorrect parameter should receive 400"""
        Ingredient.objects.create(name="carrot")
        Ingredient.objects.create(name="onion")

        res = self.client.get("/api/ingredients/search?like=arr")

        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(res.json()), 0)

    def test_get_without_query(self):
        """GET without any query should receive all the ingredients"""
        Ingredient.objects.create(name="carrot")
        Ingredient.objects.create(name="onion")

        res = self.client.get("/api/ingredients/search")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 2)


class UsersIngredientsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_only_selected_user(self):
        """Endpoint returns only the ingredients owned by the given user_id"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        u2 = User.objects.create_user(username="user2", password="testpass")
        i1 = Ingredient.objects.create(name="carrot")
        i2 = Ingredient.objects.create(name="onion")
        ui1 = UserIngredient.objects.create(user=u1, ingredient=i1)
        UserIngredient.objects.create(user=u2, ingredient=i2)

        self.setupToken(u1.username)
        res = self.client.get("/api/user/ingredients")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["id"], ui1.id)
        self.assertEqual(res.json()[0]["ingredient"]["name"], i1.name)

    def test_get_only_not_consumed(self):
        """Endpoint returns only the ingredients not consumed"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        i1 = Ingredient.objects.create(name="carrot")
        i2 = Ingredient.objects.create(name="onion")
        UserIngredient.objects.create(user=u1, ingredient=i1, consumed=True)
        ui2 = UserIngredient.objects.create(user=u1, ingredient=i2, consumed=False)

        self.setupToken(u1.username)
        res = self.client.get("/api/user/ingredients")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["id"], ui2.id)
        self.assertEqual(res.json()[0]["ingredient"]["name"], i2.name)

    def test_post_success(self):
        u = User.objects.create_user(username="user1", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "ingredient_id": i.id,
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "storage": 0,
            "expiration_date": "2022-11-19T08:19:31.193Z",
            "happiness": 40.0,
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 201)
        self.assertEqual(UserIngredient.objects.count(), 1)
        ui = UserIngredient.objects.all()[0]
        self.assertEqual(ui.user.id, u.id)
        self.assertEqual(ui.ingredient.id, i.id)
        self.assertEqual(ui.quantity_value, 1.0)
        self.assertEqual(ui.quantity_scale.id, unit.id)
        self.assertEqual(ui.storage, 0)
        self.assertEqual(ui.consumed, False)
        self.assertEqual(
            ui.expiration_date, datetime.fromisoformat("2022-11-19T08:19:31.193+00:00")
        )
        self.assertEqual(ui.happiness, 40.0)

    def test_post_missing_storage(self):
        u = User.objects.create_user(username="user1", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "ingredient_id": i.id,
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "expiration_date": "2022-11-19T08:19:31.193Z",
            "happiness": 40.0,
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 400)

    def test_post_missing_argument(self):
        u = User.objects.create_user(username="user1", password="testpass")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "storage": 0,
            "expiration_date": "2022-11-19T08:19:31.193Z",
            "happiness": 40.0,
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 400)

    def test_post_incorrect_date_format(self):
        u = User.objects.create_user(username="user1", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "ingredient_id": i.id,
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "storage": 0,
            "expiration_date": "Nov. 19, 2022",
            "happiness": 40.0,
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 400)

    def test_post_object_does_not_exist(self):
        u = User.objects.create_user(username="user1", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "ingredient_id": i.id + 1,
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "storage": 0,
            "expiration_date": "2022-11-19T08:19:31.193Z",
            "happiness": 40.0,
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 400)

    def test_post_incorrect_argument_type(self):
        u = User.objects.create_user(username="user1", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")

        data = {
            "ingredient_id": i.id,
            "quantity_value": 1.0,
            "quantity_scale_unit_id": unit.id,
            "storage": 0,
            "expiration_date": "2022-11-19T08:19:31.193Z",
            "happiness": "not happy",
        }
        self.setupToken(u.username)
        res = self.client.post("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 400)

    def test_put_full_para(self):
        u1 = User.objects.create_user(username="user1", password="testpass")
        u2 = User.objects.create_user(username="user2", password="testpass")
        i1 = Ingredient.objects.create(name="carrot")
        i2 = Ingredient.objects.create(name="milk")
        unit1 = QuantityScaleUnit.objects.create(unit="count")
        unit2 = QuantityScaleUnit.objects.create(unit="liter")
        ui = UserIngredient.objects.create(
            user=u1,
            ingredient=i1,
            quantity_value=1.0,
            quantity_scale=unit1,
            expiration_date="2022-11-19T08:19:31.193Z",
            happiness=40.0,
        )

        data = {
            "user_ingredient_id": ui.id,
            "ingredient_id": i2.id,
            "quantity_value": 1.5,
            "quantity_scale_unit_id": unit2.id,
            "consumed": True,
            "storage": 0,
            "expiration_date": "2022-11-18T08:19:31.193Z",
            "happiness": 60.0,
        }
        self.setupToken(u2.username)
        res = self.client.put("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.json()["user"], u2.id)
        self.assertEqual(res.json()["ingredient"], i2.id)
        self.assertEqual(float(res.json()["quantity_value"]), 1.5)
        self.assertEqual(res.json()["quantity_scale"], unit2.id)
        self.assertEqual(res.json()["consumed"], True)
        self.assertEqual(res.json()["storage"], 0)
        self.assertEqual(
            datetime.fromisoformat(res.json()["expiration_date"]),
            datetime.fromisoformat("2022-11-18T08:19:31.193+00:00"),
        )
        self.assertEqual(res.json()["happiness"], 60.0)

        ui = UserIngredient.objects.get(id=ui.id)
        self.assertEqual(ui.user.id, u2.id)
        self.assertEqual(ui.ingredient.id, i2.id)
        self.assertEqual(ui.quantity_value, 1.5)
        self.assertEqual(ui.quantity_scale.id, unit2.id)
        self.assertEqual(ui.consumed, True)
        self.assertEqual(ui.storage, 0)
        self.assertEqual(
            ui.expiration_date, datetime.fromisoformat("2022-11-18T08:19:31.193+00:00")
        )
        self.assertEqual(ui.happiness, 60.0)

    def test_put_partial_para(self):
        u = User.objects.create_user(username="user", password="testpass")
        i = Ingredient.objects.create(name="carrot")
        unit = QuantityScaleUnit.objects.create(unit="count")
        ui = UserIngredient.objects.create(
            user=u,
            ingredient=i,
            quantity_value=1.0,
            quantity_scale=unit,
            expiration_date="2022-11-19T08:19:31.193Z",
            happiness=40.0,
        )

        data = {
            "user_ingredient_id": ui.id,
            "quantity_value": 2.0,
            "storage": 0,
            "expiration_date": "2022-11-18T08:19:31.193Z",
            "happiness": 60.0,
        }
        self.setupToken(u.username)
        res = self.client.put("/api/user/ingredients", data, format="json")

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.json()["user"], u.id)
        self.assertEqual(res.json()["ingredient"], i.id)
        self.assertEqual(float(res.json()["quantity_value"]), 2.0)
        self.assertEqual(res.json()["quantity_scale"], unit.id)
        self.assertEqual(res.json()["consumed"], False)
        self.assertEqual(res.json()["storage"], 0)
        self.assertEqual(
            datetime.fromisoformat(res.json()["expiration_date"]),
            datetime.fromisoformat("2022-11-18T08:19:31.193+00:00"),
        )
        self.assertEqual(res.json()["happiness"], 60.0)

        ui = UserIngredient.objects.get(id=ui.id)
        self.assertEqual(ui.user.id, u.id)
        self.assertEqual(ui.ingredient.id, i.id)
        self.assertEqual(ui.quantity_value, 2.0)
        self.assertEqual(ui.quantity_scale.id, unit.id)
        self.assertEqual(ui.consumed, False)
        self.assertEqual(ui.storage, 0)
        self.assertEqual(
            ui.expiration_date, datetime.fromisoformat("2022-11-18T08:19:31.193+00:00")
        )
        self.assertEqual(ui.happiness, 60.0)


class RecipesSearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_search_exact_strict(self):
        """
        Should return recipes which use all the given ingredients and nothing more
        """
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1", num_ingredients=3)
        RecipeNutrition.objects.create(recipe=r1)
        i1 = Ingredient.objects.create(name="ingredient 1")
        i2 = Ingredient.objects.create(name="ingredient 2")
        i3 = Ingredient.objects.create(name="ingredient 3")
        RecipeIngredient.objects.create(recipe=r1, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i3)
        UserIngredient.objects.create(user=u1, ingredient=i1, consumed=False)

        self.setupToken(u1.username)

        # Recipes that use exactly (i1, i2, i3) are only r1
        res = self.client.get(
            "/api/recipes/search",
            data={
                "user": u1.id,
                "ingredient": [i1.id, i2.id, i3.id],
                "mode": "exact",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(
            res.json()[0]["ingredients"][0]["ingredient"]["in_storage"], True
        )

        # r1 uses i3, an unspecified ingredient, and thus not returned (violating 'strict')
        res = self.client.get(
            "/api/recipes/search",
            data={
                "user": u1.id,
                "ingredient": [i1.id, i2.id],  # without i3
                "mode": "exact",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 0)

        # r1 does not use i4 and thus not returned (violating 'exact')
        i4 = Ingredient.objects.create(name="ingredient 4")
        res = self.client.get(
            "/api/recipes/search",
            data={
                "user": u1.id,
                "ingredient": [i1.id, i2.id, i4.id],  # r1 does not use i4
                "mode": "exact",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 0)

    def test_search_exact_not_strict(self):
        """
        Should return recipes which use all the given ingredients (and possibly more)
        """
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1", num_ingredients=3)
        RecipeNutrition.objects.create(recipe=r1)
        i1 = Ingredient.objects.create(name="ingredient 1")
        i2 = Ingredient.objects.create(name="ingredient 2")
        i3 = Ingredient.objects.create(name="ingredient 3")
        RecipeIngredient.objects.create(recipe=r1, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i3)
        UserIngredient.objects.create(user=u1, ingredient=i1, consumed=True)

        self.setupToken(u1.username)

        # r1 uses all of the (i1, i2) and thus returned
        res = self.client.get(
            "/api/recipes/search",
            data={
                "user": u1.id,
                "ingredient": [i1.id, i2.id],  # without i3
                "mode": "exact",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(
            res.json()[0]["ingredients"][0]["ingredient"]["in_storage"], False
        )

        # No recipes use all of the (i1, i2, i4) and thus nothing returned
        i4 = Ingredient.objects.create(name="ingredient 4")
        res = self.client.get(
            "/api/recipes/search",
            data={
                "user": u1.id,
                "ingredient": [i1.id, i2.id, i4.id],  # r1 does not use i4
                "mode": "exact",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 0)

    def test_search_any_strict(self):
        """
        Should return recipes only from (some or all of) the given ingredients
        """
        r1 = Recipe.objects.create(title="recipe 1", num_ingredients=3)
        RecipeNutrition.objects.create(recipe=r1)
        r2 = Recipe.objects.create(title="recipe 2", num_ingredients=2)
        RecipeNutrition.objects.create(recipe=r2)
        i1 = Ingredient.objects.create(name="ingredient 1")
        i2 = Ingredient.objects.create(name="ingredient 2")
        i3 = Ingredient.objects.create(name="ingredient 3")
        RecipeIngredient.objects.create(recipe=r1, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i3)
        RecipeIngredient.objects.create(recipe=r2, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r2, ingredient=i2)

        # Both r1 and r2 does not use any ingredient other than (i1, i2, i3)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id, i3.id],
                "mode": "any",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 2)
        # r1 will return first based on most ingredients in list
        self.assertEqual(res.json()[0]["id"], r1.id)

        # r1 uses i3, an unspecified ingredient; thus not returned
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id],
                "mode": "any",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["id"], r2.id)

        # if the original ranking is not same with the expected result
        r3 = Recipe.objects.create(title="recipe 3", num_ingredients=3)
        i4 = Ingredient.objects.create(name="ingredient 4")
        RecipeIngredient.objects.create(recipe=r3, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r3, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r3, ingredient=i4)

        # Both r2 and r3 does not use any ingredient other than (i1, i2, i4)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id, i4.id],
                "mode": "any",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 2)
        # r3 will return first based on most ingredients in list
        self.assertEqual(res.json()[0]["id"], r3.id)
        self.assertEqual(res.json()[1]["id"], r2.id)

    def test_search_any_not_strict(self):
        """
        Should return recipes using at least one of the given ingredients
        """
        r1 = Recipe.objects.create(title="recipe 1", num_ingredients=3)
        RecipeNutrition.objects.create(recipe=r1)
        r2 = Recipe.objects.create(title="recipe 2", num_ingredients=2)
        RecipeNutrition.objects.create(recipe=r2)
        i1 = Ingredient.objects.create(name="ingredient 1")
        i2 = Ingredient.objects.create(name="ingredient 2")
        i3 = Ingredient.objects.create(name="ingredient 3")
        RecipeIngredient.objects.create(recipe=r1, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r1, ingredient=i3)
        RecipeIngredient.objects.create(recipe=r2, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r2, ingredient=i2)

        # Both r1 and r2 uses some of (i1, i2)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id],
                "mode": "any",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 2)

        # Both r1 and r2 uses some of (i1, i2, i3)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id, i3.id],
                "mode": "any",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 2)
        # r1 will return first based on most ingredients in list
        self.assertEqual(res.json()[0]["id"], r1.id)

        # Both r1 and r2 uses some of (i1,)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id],
                "mode": "any",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 2)

        # Only r1 uses some of (i3,)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i3.id],
                "mode": "any",  # any | exact
                "strict": False,
            },
        )
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["id"], r1.id)

        # if the original ranking is not same with the expected result
        r3 = Recipe.objects.create(title="recipe 3", num_ingredients=3)
        i4 = Ingredient.objects.create(name="ingredient 4")
        RecipeIngredient.objects.create(recipe=r3, ingredient=i1)
        RecipeIngredient.objects.create(recipe=r3, ingredient=i2)
        RecipeIngredient.objects.create(recipe=r3, ingredient=i4)

        # Both r2 and r3 does not use any ingredient other than (i1, i2, i4)
        res = self.client.get(
            "/api/recipes/search",
            data={
                "ingredient": [i1.id, i2.id, i4.id],
                "mode": "any",  # any | exact
                "strict": True,
            },
        )
        self.assertEqual(len(res.json()), 2)
        # r3 will return first based on most ingredients in list
        self.assertEqual(res.json()[0]["id"], r3.id)
        self.assertEqual(res.json()[1]["id"], r2.id)


class UsersRecipesHistoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_user_history(self):
        """Endpoint returns recipe history for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        u2 = User.objects.create_user(username="user2", password="testpass")

        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        r2 = Recipe.objects.create(title="recipe 2")
        RecipeNutrition.objects.create(recipe=r2)

        UserRecipeHistory.objects.create(user=u1, recipe=r1)
        UserRecipeHistory.objects.create(user=u1, recipe=r2)
        UserRecipeHistory.objects.create(user=u2, recipe=r2)

        UserRecipeFavorite.objects.create(user=u1, recipe=r1)

        self.setupToken(u1.username)
        res = self.client.get("/api/user/recipes")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 2)
        self.assertEqual(res.json()[0]["user"], u1.id)
        self.assertEqual(res.json()[0]["recipe"]["user_favorite"], False)
        self.assertEqual(res.json()[1]["recipe"]["user_favorite"], True)

    def test_post_user_history(self):
        """Endpoint adds recipe history item for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")

        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)

        self.setupToken(u1.username)
        res = self.client.post("/api/user/recipes", data={"recipe_id": r1.id})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["user"], u1.id)
        self.assertEqual(res.json()["recipe"], r1.id)
        self.assertEqual(res.json()["cooked"], False)

    def test_put_user_history(self):
        """Endpoint edits recipe history item for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        UserRecipeHistory.objects.create(user=u1, recipe=r1)

        self.setupToken(u1.username)
        res = self.client.put(
            "/api/user/recipes",
            data={"recipe_id": r1.id, "cooked": True},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["user"], u1.id)
        self.assertEqual(res.json()["recipe"], r1.id)
        self.assertEqual(res.json()["cooked"], True)

    def test_delete_user_history(self):
        """Endpoint deletes recipe history item for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        ur1 = UserRecipeHistory.objects.create(user=u1, recipe=r1)

        self.setupToken(u1.username)
        res = self.client.delete(
            "/api/user/recipes",
            data={"user_recipe_history_id": ur1.id},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["deleted"], 1)


class UsersStatisticsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_user_statistics(self):
        """Endpoint returns favorite recipes information"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        i1 = Ingredient.objects.create(name="ingredient 1")
        UserIngredient.objects.create(user=u1, ingredient=i1)
        UserRecipeFavorite.objects.create(user=u1, recipe=r1)
        UserRecipeHistory.objects.create(user=u1, recipe=r1, cooked=True)

        self.setupToken(u1.username)
        res = self.client.get("/api/user/stats")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["user"], u1.id)
        self.assertEqual(res.json()["all_cooked"], 1)
        self.assertEqual(res.json()["all_liked"], 1)
        self.assertEqual(res.json()["all_ingredients"], 1)


class UsersFavoriteRecipesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def setupToken(self, username, password="testpass"):
        _res = self.client.post(
            "/api/token",
            data={"username": username, "password": password},
            format="json",
        )
        token = _res.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_user_favorites(self):
        """Endpoint returns favorite recipes information"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        UserRecipeFavorite.objects.create(user=u1, recipe=r1)

        self.setupToken(u1.username)
        res = self.client.get("/api/user/favorite")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["user"], u1.id)
        self.assertEqual(res.json()[0]["recipe"]["id"], r1.id)

    def test_post_user_favorites(self):
        """Endpoint adds recipe history item for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")

        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)

        self.setupToken(u1.username)
        res = self.client.post("/api/user/favorite", data={"recipe_id": r1.id})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["user"], u1.id)
        self.assertEqual(res.json()["recipe"], r1.id)

    def test_delete_user_favorites(self):
        """Endpoint deletes recipe history item for a user"""
        u1 = User.objects.create_user(username="user1", password="testpass")
        r1 = Recipe.objects.create(title="recipe 1")
        RecipeNutrition.objects.create(recipe=r1)
        UserRecipeFavorite.objects.create(user=u1, recipe=r1)

        self.setupToken(u1.username)
        res = self.client.delete(
            "/api/user/favorite",
            data={"recipe_id": r1.id},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["deleted"], 1)


class RandomRecipeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_random_recipe(self):
        """Return a random recipe"""
        r1 = Recipe.objects.create(title="recipe 1", num_ingredients=3)
        RecipeNutrition.objects.create(recipe=r1)
        r2 = Recipe.objects.create(title="recipe 2", num_ingredients=2)
        RecipeNutrition.objects.create(recipe=r2)
        res = self.client.get("/api/recipes/random")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["id"] in [r1.id, r2.id])
