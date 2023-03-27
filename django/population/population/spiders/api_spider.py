import json
import logging
import re
from datetime import datetime

import lxml.html
import lxml.html.clean
import parsedatetime
import requests  # just to check res.status without ALLOWED_DOMAIN restriction
import scrapy
import spacy  # for nlp
from api.models import Ingredient
from asgiref.sync import sync_to_async
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)

from ..items import (
    IngredientItem,
    QuantityScaleUnitItem,
    RecipeIngredientItem,
    RecipeItem,
    RecipeNutritionItem,
    RecipeTagItem,
    TagItem,
)
from ..settings import EDAMAM_APPID, EDAMAM_APPKEY, EDAMAM_RECURSION

logging.basicConfig(filename="spider.log", encoding="utf-8", level=logging.INFO)
nlp = spacy.load("en_core_web_md")

tag_map = {  # 'Edamam-label': 'our-db-category-name'
    "dietLabels": "diet",
    "healthLabels": "health",
    "cuisineType": "cuisine",
    "mealType": "meal",
    "dishType": "dish",
}


class RecipeSite:
    def __init__(self, url, get_image):
        self.url = url
        self.get_image = get_image


RECIPE_SITES = {
    "bbc_good_food": RecipeSite(
        "www.bbcgoodfood.com",
        lambda response: response.css("section.post-header img.image__img").attrib[
            "src"
        ],
    ),
    "serious_eats": RecipeSite(
        "www.seriouseats.com",
        lambda response: response.css("div.article-content img.primary-image").attrib[
            "src"
        ],
    ),
    "food_network": RecipeSite(
        "www.foodnetwork.com",
        lambda response: (
            "https:"
            + response.css("div.recipe-lead img.m-MediaBlock__a-Image").attrib["src"]
        ),
    ),
    "food52": RecipeSite(
        "food52.com",
        lambda response: response.css("div#recipeCarouselRoot picture source")
        .attrib["data-srcset"]
        .split(",")[0],
    ),
    "martha": RecipeSite(
        "www.marthastewart.com",
        lambda response: response.css(
            "aside.recipe-tout-image div.inner-container button"
        ).attrib["data-image"],
    ),
    "bbc.co.uk": RecipeSite(
        "www.bbc.co.uk",
        lambda response: response.css("div.recipe-media img").attrib["src"],
    ),
    "all_recipes": RecipeSite(
        "www.allrecipes.com",
        lambda response: response.css("div.article-content img").attrib["src"],
    ),
    "delish": RecipeSite(
        "www.delish.com",
        lambda response: response.css("div.content-lead img").attrib["src"],
    ),
    "cook_str": RecipeSite(
        "www.cookstr.com",
        lambda response: "https:" + response.css("div.mainImg img").attrib["src"],
    ),
    "honest_cooking": RecipeSite(
        "honestcooking.com",
        lambda response: response.css("div.post-content img").attrib["data-src"],
    ),
}


class FoodString:
    def __init__(self, string: str) -> None:
        self.original_string = string

    def __convert_plural_to_singular(self, string: str):
        _parsed = nlp(string)
        _r = ""
        for _t in _parsed:
            lemma = _t.text
            if _t.tag_ in ["NNS", "NNPS"]:
                lemma = _t.lemma_
            if re.search(r"\w", lemma) is not None:
                _r += f"{lemma} "
        _r = _r.strip()

        if len(string.split()) != len(_r.split()):
            logging.log(
                logging.ERROR, f"String '{string}' and '{_r}' are not coherent."
            )
        return _r

    @property
    def api_request_string(self):
        return (
            re.sub(r"[^a-zA-Z0-9\s]+", "", self.original_string).replace(" ", "+")
            if self.original_string
            else ""
        )

    @property
    def basic_proccessed_string(self):
        return (
            "" if self.original_string is None else self.original_string.strip().lower()
        )

    @property
    def recipe_title_string(self):
        _r = self.basic_proccessed_string
        # handle `&` in recipes
        _r = re.sub(r"([a-zA-Z])&([a-zA-Z])", r"\1 and \2", _r)
        _r = re.sub(r"\s+&\s+", " and ", _r)
        # handle 'recipe' in title
        _r = re.sub(r"\(?\s*recipe\)?s*\)?", "", _r)
        return _r

    @property
    def ingredient_name_string(self):
        _r = self.basic_proccessed_string
        _r = re.sub(r"%", " precent ", _r)
        _r = re.sub(r"[^\w\d.,']", " ", _r)
        _r = re.sub(r"\s+", " ", _r)
        return self.__convert_plural_to_singular(_r)

    @property
    def ingredient_query_string(self):
        _r = self.basic_proccessed_string
        _r = re.sub(r"essence", "extract", _r)
        _r = re.sub(r"\sroll[\W]?|\sbun[\W]?", " roll or bun ", _r)
        return _r

    @property
    def unit_scale_string(self):
        _r = self.basic_proccessed_string
        _r = re.sub(r"[\W]", "", _r)
        return _r if _r.strip() not in ["", "naan"] else "unknown"


class APISpider(scrapy.Spider):
    name = "api_spider"
    cleaner = lxml.html.clean.Cleaner(style=True)
    allowed_domains = [
        "www.themealdb.com",
        "api.edamam.com",
        "www.stilltasty.com",
        *list(map(lambda site: site.url, RECIPE_SITES.values())),
    ]

    def __init__(self, **kwargs):
        """Constructor

        :param letter: Letter('a') or a range of letters ('a-z') for MealDB
        :param edamam: Comma-separated keywords for Edamam
        """

        if not kwargs:  # defaults to "letter=a" option
            kwargs = {"letter": "a"}

        self.kwargs = kwargs

    def start_requests(self):
        """Returns the initial requests"""

        if "edamam" in self.kwargs:
            return self.requestsToEdamam(self.kwargs["edamam"].split(","))

        # default case
        return self.requestsToMealDBFromLetter(self.kwargs["letter"])

    def handleErrors(self, failure):
        # errback handling for requests, attached to the request parameters

        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)

        elif failure.check(ConnectionRefusedError):
            # the connection wasrefused by the other side.
            response = failure.request
            self.logger.error("ConnectionRefusedError on %s", response.url)

        else:
            # log all other failures just in case
            self.logger.error(repr(failure))

    def requestsToMealDBFromLetter(self, letter):
        """Returns an array of reqeusts to MealDB by the first letter

        :param letter: Letter('a') or a range of letters ('a-z') for MealDB
        """

        if len(letter) == 1:
            letter = f"{letter}-{letter}"

        if re.search(r"^[a-z]-[a-z]$", letter) is None:
            raise ValueError(f"Argument 'letter' ({repr(letter)}) is ill-formed")

        first, last = letter[0], letter[-1]

        return [
            scrapy.Request(
                f"https://www.themealdb.com/api/json/v1/1/search.php?f={chr(c)}",
                callback=self.handleMealDB,
                priority=5,
            )
            for c in range(ord(first), ord(last) + 1)
        ]

    def requestsToEdamam(self, keywords):
        """Returns an array of reqeusts to Edamam with the given keywords"""

        return [
            scrapy.Request(
                f"https://api.edamam.com/search?app_id={EDAMAM_APPID}&app_key={EDAMAM_APPKEY}&q={kw}",
                callback=self.handleEdamam,
                priority=5,
            )
            for kw in keywords
        ]

    def handleMealDB(self, response, **kwargs):
        """Response handler for MealDB

        Parse the response JSON and make requests to Edamam.
        """

        # Convert response text to dict
        body = json.loads(response.body)

        if body["meals"] is None:
            return

        for meal in body["meals"]:
            keyword = FoodString(meal["strMeal"]).api_request_string
            yield scrapy.Request(
                f"https://api.edamam.com/search?app_id={EDAMAM_APPID}&app_key={EDAMAM_APPKEY}&q={keyword}",
                callback=self.handleEdamam,
                errback=self.handleErrors,
                priority=10,
            )

    def handleEdamam(self, response, **kwargs):
        """Response handler for Edamam

        - Parse the response JSON and create RecipeItem
        - Make a request to the recipe URL for verification
        """

        # Convert response text to dict
        body = json.loads(response.body)

        # Go over each found recipe
        for hit in body["hits"]:
            # Filter out recipes with not enough information
            if not self.__recipe_check_criteria(hit["recipe"]):
                continue

            recipe = RecipeItem(
                title=FoodString(hit["recipe"]["label"]).recipe_title_string,
                recipe_url=hit["recipe"]["url"],
                cook_minute=hit["recipe"]["totalTime"],
                num_servings=int(hit["recipe"]["yield"]),
                num_ingredients=len(
                    {
                        FoodString(i["food"]).ingredient_name_string
                        for i in hit["recipe"]["ingredients"]
                    }
                ),
            )

            yield scrapy.Request(
                hit["recipe"]["url"],
                callback=self.handleRecipePage,
                errback=self.handleErrors,
                priority=15,
                cb_kwargs={"recipeItem": recipe, "hitRecipe": hit["recipe"]},
            )

    async def handleRecipePage(self, response, **kwargs):
        """Response handler for every recipe URLs

        - Parse the response HTML and verify recipe's title matches
        - If it does, yield RecipeItem and make requests to Edamam
        """

        doc = lxml.html.fromstring(response.body)
        doc = self.cleaner.clean_html(doc)  # convert &nbsp; etc.
        text = re.sub("\xa0", " ", doc.text_content().lower())  # NOTE: need more?
        text = re.sub(r"\n|\r", " ", text)

        orig_title = re.sub(r"\(?recipes?\)?", "", kwargs["hitRecipe"]["label"].lower())
        if orig_title not in text:
            logging.log(
                logging.DEBUG,
                f"could not find {repr(orig_title)} at {response.url}",
            )
            return  # assume the recipe content is gone, skip further exec

        logging.log(
            logging.INFO,
            f"Recipe: {kwargs['recipeItem']['title']}, ({kwargs['recipeItem']['num_ingredients']} ingr.)",
        )
        recipe = kwargs["recipeItem"]

        # fetch image_url and update it
        recipe["image_url"] = self.__get_image(response)
        if recipe["image_url"] == "":  # if failed
            logging.log(logging.WARNING, "Failed to find the image_url")
            return  # skip further exec

        # visit the image_url and continue only if status == 200
        if not self.__status_matches(recipe["image_url"], 200):
            logging.log(
                logging.WARNING,
                f"Failed to fetch the extracted image_url: {recipe['image_url']}",
            )
            return

        yield recipe

        # yield nutrition
        n_srv = recipe["num_servings"]
        nut = kwargs["hitRecipe"]["totalNutrients"]
        nutrition = RecipeNutritionItem(
            recipe=recipe.instance,
            calories_kcal_per_serving=nut["ENERC_KCAL"]["quantity"] / n_srv,
            fat_gram_per_serving=nut["FAT"]["quantity"] / n_srv,
            carbs_gram_per_serving=nut["CHOCDF"]["quantity"] / n_srv,
            protein_gram_per_serving=nut["PROCNT"]["quantity"] / n_srv,
        )
        yield nutrition

        # yield recipe_tag
        for (label, category) in tag_map.items():
            if label in kwargs["hitRecipe"]:
                for name in kwargs["hitRecipe"][label]:
                    tag = TagItem(
                        name=FoodString(name).basic_proccessed_string, category=category
                    )
                    # tag is auto-saved by yielding recipe_tag below
                    recipe_tag = RecipeTagItem(recipe=recipe.instance, tag=tag.instance)
                    yield recipe_tag

        # call shelf-life for each ingredient
        for ingredient_obj in kwargs["hitRecipe"]["ingredients"]:
            ingredient_string = FoodString(ingredient_obj["food"])

            db_ingredient = await sync_to_async(
                Ingredient.objects.filter(
                    name=ingredient_string.ingredient_name_string
                ).first
            )()
            if db_ingredient:  # if already exists in DB
                logging.log(
                    logging.INFO,
                    f"\t#{recipe.instance.id} (from db) found ingredient: "
                    + ingredient_string.basic_proccessed_string.upper(),
                )
                quantity_scale = QuantityScaleUnitItem(
                    unit=FoodString(ingredient_obj["measure"]).unit_scale_string,
                    description="",
                )
                yield quantity_scale
                yield RecipeIngredientItem(
                    recipe=recipe.instance,
                    ingredient=db_ingredient,
                    quantity_value=ingredient_obj["quantity"],
                    quantity_scale=quantity_scale.instance,
                    weight=ingredient_obj["weight"],
                )

                continue  # skip issuing request to Still-Tasty

            logging.log(
                logging.INFO,
                f"\t#{recipe.instance.id} Ingredient: {ingredient_string.basic_proccessed_string.upper()}",
            )
            yield scrapy.FormRequest(
                url="https://www.stilltasty.com/searchitems/search",
                formdata={"search": ingredient_string.ingredient_query_string},
                callback=self.handleStillTastySearch,
                errback=self.handleErrors,
                dont_filter=True,
                priority=20,
                cb_kwargs={
                    "recipe": recipe,
                    "ingredientObj": ingredient_obj,
                    "ingredient": ingredient_string.ingredient_name_string,
                    "query": ingredient_string.ingredient_query_string,
                },
            )

    def __recipe_check_criteria(self, recipe):
        if not recipe["yield"] or recipe["yield"] <= 0:
            return False
        if not recipe["totalTime"] or recipe["totalTime"] <= 0:
            return False
        # if recipe title not all ascii ignore
        if not all(ord(c) < 128 for c in recipe["label"]):
            return False
        # if recipe title is too long ignore (save further req in vain)
        max_len = RecipeItem.django_model._meta.get_field("title").max_length
        if len(recipe["label"]) > max_len:
            return False
        return True

    def handleStillTastySearch(self, form_response: scrapy.FormRequest, **kwargs):
        """Handle StillTasty search requests.
        Extracting potential matches and yielding requests for each item page.

        Args:
            form_response (scrapy.FormResponse): the response of the request

        Returns:
            scrapy.FormRequest: requests for scrapy queue if any matches exist

        Yields:
            scrapy.Request: the item requests for item details
        """
        # Get possible ingredient entries
        links = form_response.css("p[class=srclisting] a::attr(href)").getall()
        names = form_response.css("p[class=srclisting] a::text").getall()

        assert len(links) == len(names)

        urls = self.__collect_valid_ingredient_info_urls(kwargs["query"], links, names)

        if len(urls) <= 0:
            logging.log(
                logging.WARNING,
                f"No results for '{kwargs['ingredient']}' ({kwargs['query']}) on StillTasty...",
            )
            for r in self.__reissue_search_from_ingredient_query(kwargs):
                yield r
            return

        # issue requests for all candidates
        for _u in urls:
            yield scrapy.Request(
                url=_u,
                callback=self.handleStillTastyItem,
                errback=self.handleErrors,
                dont_filter=True,
                priority=20,
                cb_kwargs={
                    "recipe": kwargs["recipe"],  # recipe instance
                    "ingredientObj": kwargs["ingredientObj"],  # ingredient info object
                    "ingredient": kwargs["ingredient"],  # ingredient name
                },
            )

    def __reissue_search_from_ingredient_query(self, kwargs):
        requests = []
        parsed = nlp(kwargs["query"])
        logging.log(
            logging.INFO,
            f"Text '{kwargs['query']}', {sum(1 for _ in parsed.noun_chunks)} noun chunks.",
        )
        for x in parsed.noun_chunks:
            logging.log(
                logging.INFO,
                f"\tCHUNK: '{x.text}' (lemma={x.lemma_}), root= '{x.root.text}' root.dep= ({x.root.dep_}) root.lemma= ({x.root.lemma_})",
            )

        # send out requests for noun chunks in the ingredient name
        for x in parsed.noun_chunks:
            if x.text != kwargs["query"]:
                logging.log(
                    logging.INFO,
                    f"... Searching for '{x.text}' instead.",
                )
                requests.append(
                    scrapy.FormRequest(
                        url="https://www.stilltasty.com/searchitems/search",
                        formdata={"search": x.text},
                        callback=self.handleStillTastySearch,
                        dont_filter=True,
                        priority=20,
                        cb_kwargs={
                            "recipe": kwargs["recipe"],
                            "ingredientObj": kwargs["ingredientObj"],
                            "ingredient": kwargs["ingredient"],
                            "query": x.text,
                        },
                    )
                )
            if x.root.text != x.text:
                logging.log(
                    logging.INFO,
                    f"... Searching for '{x.root.text}' instead.",
                )
                requests.append(
                    scrapy.FormRequest(
                        url="https://www.stilltasty.com/searchitems/search",
                        formdata={"search": x.root.text},
                        callback=self.handleStillTastySearch,
                        dont_filter=True,
                        priority=20,
                        cb_kwargs={
                            "recipe": kwargs["recipe"],
                            "ingredientObj": kwargs["ingredientObj"],
                            "ingredient": kwargs["ingredient"],
                            "query": x.root.text,
                        },
                    )
                )
        return requests

    def __collect_valid_ingredient_info_urls(self, ingredient, links, names):
        if len(links) <= 1:
            logging.log(
                logging.INFO,
                f"One item or less found, links={links}",
            )
            return links

        urls = []
        for i, _l in enumerate(links):
            logging.log(
                logging.INFO,
                f"#{i}, ({names[i]}): ...",
            )
            _s = self.__get_ingredient_relation_score(names[i].lower(), ingredient)
            urls.append((_s, _l))

        urls.sort(key=lambda x: x[0], reverse=True)
        logging.log(logging.INFO, f"Ingredient URLs ({len(urls)}): {urls[:4]}...")

        return [_u for _s, _u in urls if _s >= urls[0][0]]

    def __get_ingredient_relation_score(self, name, ingredient):
        _sim = 0  # lexical similarity
        _type = 0  # type verification

        name = re.sub(r"[-–—−]", "-", name)
        name = re.sub(r"\s+", " ", name)

        srch = re.search(
            r"^([^,]+),?(.*)\s\-\s(.*)$",
            name,
        )

        ingredient = FoodString(ingredient).ingredient_name_string
        name = FoodString(
            srch.group(1)
            if srch is not None
            else re.search(r"^([^,]+),?(.*)$", name).group(1)
        ).ingredient_name_string

        logging.log(
            logging.INFO,
            f"\tComparing #'{ingredient}' and ?'{name}'... Similarity: {nlp(name).similarity(nlp(ingredient))}",
        )

        _sim = nlp(name).similarity(nlp(ingredient))
        _type = (
            1
            if (
                not srch
                or len(re.findall(r"(\bkosher\b|\braw\b|\bopene?d?\b)", srch.group(3)))
                > 0
            )
            else 0
        )
        return _sim + _type if _sim > 0.5 else _type

    def handleStillTastyItem(self, response, **kwargs):
        """Handles StillTasty item information requests.
        Extracts methods of storage and storage duration for items using a queue of requests.

        Args:
            response (scrapy.Response): the response of the request

        Yields:
            IngredientItem: The ingredient item over Django ORM
            RecipeIngredientItem: The recipe to ingredient item over Django ORM
        """
        methods = response.css(
            "div[class~=food-inside] > div:first-child span::text"
        ).getall()
        life = response.css(
            "div[class~=food-inside] > div:nth-child(2) span::text"
        ).getall()

        # Parse shelf-life values from StillTasty
        shelf_life = self.__extract_shelf_life_from_data(
            response, kwargs, methods, life
        )

        ingredient = IngredientItem(
            name=kwargs["ingredient"],
            info_url=response.url,
            image_url=kwargs["ingredientObj"]["image"],
        )

        # add category when available
        if kwargs["ingredientObj"]["foodCategory"]:
            ingredient["category"] = FoodString(
                kwargs["ingredientObj"]["foodCategory"]
            ).basic_proccessed_string
        # add shelf-life when available
        if shelf_life is not None:
            ingredient["pantry_days"] = (
                shelf_life["pantry"] if "pantry" in shelf_life.keys() else None
            )
            ingredient["refrigerator_days"] = (
                shelf_life["refrigerator"]
                if "refrigerator" in shelf_life.keys()
                else None
            )
            ingredient["freezer_days"] = (
                shelf_life["freezer"] if "freezer" in shelf_life.keys() else None
            )
        yield ingredient
        quantity_scale = QuantityScaleUnitItem(
            unit=FoodString(kwargs["ingredientObj"]["measure"]).unit_scale_string,
            description="",
        )
        yield quantity_scale
        yield RecipeIngredientItem(
            recipe=kwargs["recipe"].instance,
            ingredient=ingredient.instance,
            quantity_value=kwargs["ingredientObj"]["quantity"],
            quantity_scale=quantity_scale.instance,
            weight=kwargs["ingredientObj"]["weight"],
        )

        if EDAMAM_RECURSION:
            # send a recursive request to Edamam, using the ingredient name
            yield scrapy.Request(
                f"https://api.edamam.com/search?app_id={EDAMAM_APPID}&app_key={EDAMAM_APPKEY}&q={FoodString(kwargs['ingredient']).api_request_string}",
                callback=self.handleEdamam,
                errback=self.handleErrors,
                priority=0,  # set the lowest priority
            )

    def __extract_shelf_life_from_data(self, response, kwargs, methods, life):
        shelf_life = {}
        for i, _m in enumerate(methods):
            life_string = FoodString(life[i]).basic_proccessed_string
            method_string = FoodString(_m).basic_proccessed_string
            if "keeps indefinitely" in life_string:
                logging.log(
                    logging.INFO,
                    f"Ingredient '{kwargs['ingredient']}' keeps indefinitely ({method_string.upper()}).",
                )
                return None
            life_text_srch = re.search(
                r"(\d+)(\-\d+)?\s*(days?|weeks?|months?|years?)", life_string
            )

            if not life_text_srch or life_text_srch.lastindex < 3:
                logging.log(
                    logging.WARNING,
                    f"Item '{kwargs['ingredient']}' has issue with Method '{method_string.upper()}' on '{life_string}'",
                )
                continue
            life_text = f"{life_text_srch.group(1)} {life_text_srch.group(3)}"
            life_days = (
                parsedatetime.Calendar().parseDT(datetimeString=life_text)[0]
                - datetime.now()
            ).days + 1
            shelf_life[method_string] = life_days

        return shelf_life

    def __get_image(self, response):
        """Returns the image url or an empty string, if not found"""

        for _site in RECIPE_SITES.values():
            if _site.url in response.url:
                try:
                    return _site.get_image(response)
                except Exception:
                    logging.log(
                        logging.WARNING,
                        f"Failed to parse image URL on {response.url}",
                    )
                    return ""

        return ""  # fallback

    def __status_matches(self, url, expected_status):
        """Returns True if the actual status code matches the expected one"""
        res = requests.get(url)
        return res.status_code == expected_status
