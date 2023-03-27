# API specification

## obtain tokens (access token and refresh token)

- Request:

  - method: `POST`
  - endpoint: `/token`
  - header: `"Content-Type: application/json"`
  - body:
    - `username: string`
    - `password: string`

- Response:

  - if authentication succeeds
    - status: `200`
    - body:
      - `refresh: string`: refresh token
      - `access: string`: access token
  - else (authentication fails)
    - status: `401`
    - body:
      - `detail: string`

- Exapmle:
  - success case:
    - request: `curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "testpass"}' http://localhost:8000/api/token`
    - response: `{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI2ODg5MCwiaWF0IjoxNjcxMTgyNDkwLCJqdGkiOiJlOGVjNGZlZDBmNmI0ZjljOTJkY2I4ZDJkN2Q0OTc5YiIsInVzZXJfaWQiOjF9.4wWrhpAgl5Z-cSPGUdFahmEAKw3GEcsCWIORp9M66IA","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMTgyNzkwLCJpYXQiOjE2NzExODI0OTAsImp0aSI6IjA4OTA4Y2QwMGI1ZjRkMzE5YjIzYjRjMWFkMGQwYTU3IiwidXNlcl9pZCI6MX0.1-0fpops_IYLTO1ZKXjJjYLDkz_8bxlmjj564MF2MkQ"}`
  - failure case:
    - request: `curl -X POST -H "Content-Type: application/json" -d '{"username": "aaaaa", "password": "p"}' http://localhost:8000/api/token`
    - response: `{"detail":"No active account found with the given credentials"}`

## renew the access token

- Request:

  - method: `POST`
  - endpoint: `/token/refresh`
  - header: `"Content-Type: application/json"`
  - body:
    - `refresh: string`: your refresh token

- Response:

  - if authentication succeeds
    - status: `200`
    - body:
      - `access: string` access token
  - else (authentication fails)
    - status: `401`
    - body:
      - `detail: string`
      - `code: string`

- Example:
  - success case:
    - request: `curl -i -X POST -H "Content-Type: application/json" -d '{"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI2OTk0NiwiaWF0IjoxNjcxMTgzNTQ2LCJqdGkiOiJlMzAwZWYzOGU5MjM0ZmJiOTcyMTE2MzNjMDExY2M4MCIsInVzZXJfaWQiOjF9.YFroFChUDWyK2eEJlAmgSTCvD2gzi6FvbNp7lQ3a1vs"}' http://localhost:8000/api/token/refresh`
    - response: `{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMTgzODk1LCJpYXQiOjE2NzExODM1NDYsImp0aSI6Ijk4YWZmZDUwMjZlMTQ4NmRiNDY4ZmE2MmI4ZTdiNzdmIiwidXNlcl9pZCI6MX0.CQxHIC1ruS6M8KXu5Bebrb5w8kr1MvENw1o_DI82Txc"}`
  - failure case:
    - request: `curl -i -X POST -H "Content-Type: application/json" -d '{"refresh": "json.web.token"}' http://localhost:8000/api/token/refresh`
    - response: `{"detail":"Token is invalid or expired","code":"token_not_valid"}`

## validate the token

- Request:

  - method: `POST`
  - endpoint: `/token/verify`
  - header: `"Content-Type: application/json"`
  - body:
    - `token: string`: your token, either access token or refresh token

- Response:

  - if authentication succeeds
    - status: `200`
    - body: empty object (`{}`)
  - else (authentication fails)
    - status: `401`
    - body:
      - `detail: string`
      - `code: string`

- Example:
  - success case:
    - request: `curl -i -X POST -H "Content-Type: application/json" -d '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMTg0NDA3LCJpYXQiOjE2NzExODQxMDcsImp0aSI6ImM1YmY1MjUxOGE3ODQ4MTdiODdmZGQyNWI1NGM4YTdlIiwidXNlcl9pZCI6MX0.3Mt-i8Uf5R58ggt62xXmWmcV2TOOgbUQB5VhGx2qOIw"}' http://localhost:8000/api/token/verify`
    - response: `{}`
  - failure case:
    - request: `curl -i -X POST -H "Content-Type: application/json" -d '{"token": "json.web.token"}' http://localhost:8000/api/token/verify`
    - response: `{"detail":"Token is invalid or expired","code":"token_not_valid"}`

## add a new user

- Request:
  - method: POST
  - endpoint: /signup
  - body:
    - `username: string`
    - `password: string`
- Response:

  - success case:
    - status: 201
    - body:
      - `user_id: string`
  - failure case:
    - status: 400
      - body:
        - `detail?: string`
        - `username?: string[]` array of errors for `useraname` field
        - `password?: string[]` array of errors for `password` field

- Example:
  - success case:
    - request: `curl -X POST -H 'Content-Type: application/json' -d '{"username": "user11", "password": "testpass"}' http://localhost:8000/api/signup`
    - response: `{"user_id":9}`
  - failure case:
    - request: `curl -X POST -H 'Content-Type: application/json' -d '{"username": "user11", "password": "testpass"}' http://localhost:8000/api/signup`
    - response: `{"username":["A user with that username already exists."]}`

## get ingredient information

- HTTP request: `GET user/ingredients`
- Return value

  `UserIngredient[]`: The list of not consumed ingredients owned by `user_id` where

  ```javascript
  UserIngredient =
  {
    integer id,
    bool consumed,
    string created_date,
    string? expiration_date,
    float? happiness,
    integer user,
    Ingredient ingredient
  }
  ```

  ("?" indicates an option.)

  where

  ```javascript
  Ingredient =
  {
    integer id,
    string name,
    string? info_url,
    string? image_url,
    string? category,
    integer? pantry_days,
    integer? refrigerator_days,
    integer? freezer_days
  }
  ```

  - Example

  ```json
  [
    {
      "id": 1,
      "consumed": false,
      "created_date": "2022-12-04T10:28:02.663692+09:00",
      "expiration_date": null,
      "happiness": null,
      "user": 1,
      "ingredient": {
        "id": 306093,
        "name": "water",
        "info_url": "https://www.stilltasty.com/fooditems/index/19047",
        "image_url": "https://www.edamam.com/food-img/5dd/5dd9d1361847b2ca53c4b19a8f92627e.jpg",
        "category": "water",
        "pantry_days": null,
        "refrigerator_days": 4,
        "freezer_days": null
      }
    }
  ]
  ```

## add a new ingredient

- HTTP request: `POST user/ingredients`
- Arguments

  - `integer ingredient_id`
  - `float quantity_value`
  - `integer quantity_scale_unit_id`
  - `integer storage`: either `0` (pantry), `1` (refrigerator), or `2` (freezer)
  - `string expiration_date`: format of YYYY-MM-DDThh:mm:ss.sssZ. (ISO 8601 Date string) It represents date and time in UTC. It can be obtained by `JSON.stringify`. For example,

    ```javascript
    d = new Date(); //Sat Nov 19 2022 17:19:31 GMT+0900 (Japan Standard Time)
    console.log(JSON.stringify(d)); //"2022-11-19T08:19:31.193Z"
    ```

  - `float happiness`

- Return value
  - If successful,
    - Returns the added `UserIngredient` (status code: 201)
  - If not successful,
    - `string error_message` (status code: 400)

## edit ingredient information

- HTTP request: `PUT user/ingredients`
- Arguments
  - `integer user_ingredient_id`
  - `integer? ingredient_id`
  - `float? quantity_value`
  - `integer? quantity_scale_unit_id`
  - `bool? consumed`
  - `integer? storage`: either `0` (pantry), `1` (refrigerator), or `2` (freezer)
  - `string? expiration_date`
  - `float? happiness`
- Note
  - When optional arguments are missing, those fields do not change.
- Return value

  - If successful,

    ```javascript
    //edited user ingredient
    {
      integer id,
      integer user, //user id
      integer ingredient, //ingredient id
      string? quantity_value, //e.g., "1.50"
      integer? quantity_scale, //quantity scale unit id
      bool consumed,
      integer storage,
      string created_date,
      string? expiration_date,
      float? happiness
    }
    ```

    (status code: 200)

  - If not successful,
    - `string error_message` (status code: 400)

## search ingredients

- HTTP request: `GET ingredients/search`

- Argument

  - `string icontains`: string that names of ingredients should contain (case-insensitive)

- Response 200

  - List of matched ingredients

    Type of ingredient (property with "?" indicates it may not exist):

    ```text
    id: int
    name: string
    info_url?: string (URL)
    image_url?: string (URL)
    category?: string
    pantry_days?: int
    refrigerator_days?: int
    freezer_days?: int
    ```

## search recipes

- HTTP request: `GET recipes/search`
- Arguments
  - `string[] ingredient_list`: list of names of ingredients
  - `string mode` : `any` or `exact` to include any subgroup or exactly all ingredients.
  - `boolean strict` : exclude or include unspecified ingredients
- Return value

  - List of recipes that match the search criteria.

- Example:

  ```json
  {
    "id": 1,
    "title": "recipe 1",
    "recipe_url": "",
    "image_url": "",
    "cook_minute": "None",
    "num_servings": "None",
    "language": "en",
    "num_ingredients": 3,
    "favorite": false,
    "cooked": false,
    "users_cooked": 0,
    "users_liked": 0,
    "ingredients": [
      {
        "id": 1,
        "name": "ingredient 1",
        "info_url": "None",
        "image_url": "None",
        "category": "foods",
        "pantry_days": "None",
        "refrigerator_days": "None",
        "freezer_days": "None",
        "in_storage": false
      },
      {
        "id": 2,
        "name": "ingredient 2",
        "info_url": "None",
        "image_url": "None",
        "category": "foods",
        "pantry_days": "None",
        "refrigerator_days": "None",
        "freezer_days": "None",
        "in_storage": false
      },
      {
        "id": 3,
        "name": "ingredient 3",
        "info_url": "None",
        "image_url": "None",
        "category": "foods",
        "pantry_days": "None",
        "refrigerator_days": "None",
        "freezer_days": "None",
        "in_storage": false
      }
    ]
  }
  ```

````

## get recipe information of user (history)

- HTTP request: `GET user/recipes`
- Return value

  ```javascript
  {
    History[]
  }
````

where

```javascript
History =
{
  integer id,
  string access_date, //ISO 8601
  bool cooked,
  integer user,
  Recipe recipe,
  bool favorite,
}
```

where

```javascript
Recipe =
{
  integer id,
  string title,
  string? recipe_url,
  string? image_url,
  integer? cook_minute,
  integer? num_servings,
  string language,
  integer? num_ingredients
}
```

- Example

```json
{
    [
        {
            "id": 2,
            "access_date": "2022-12-08T21:17:40.154392+09:00",
            "cooked": false,
            "user": 39,
            "recipe": {
                "id": 67380,
                "title": "recipe 2",
                "recipe_url": "",
                "image_url": "",
                "cook_minute": null,
                "num_servings": null,
                "language": "en",
                "num_ingredients": null
            },
            "favorite": false
        },
        {
            "id": 1,
            "access_date": "2022-12-08T21:17:33.920801+09:00",
            "cooked": false,
            "user": 39,
            "recipe": {
                "id": 67379,
                "title": "recipe 1",
                "recipe_url": "",
                "image_url": "",
                "cook_minute": null,
                "num_servings": null,
                "language": "en",
                "num_ingredients": null
            },
            "favorite": true
        }
    ]
}
```

## add recipe history information of user

- HTTP request: `POST user/recipes`
- Arguments

  - `integer recipe_id`

- Return value
  The new inserted history element

## edit recipe history information of user

- HTTP request: `PUT user/recipes`
- Arguments

  - `integer user_recipe_history_id`
  - `boolean cooked`

- Return value
  The edited history element

## delete recipe information of user

- HTTP request: `DELETE user/recipes`
- Arguments

  - `integer user_recipe_history_id`

- Return value

```javascript
{
    string message,
    integer deleted // the number of deleted items (should be 1)
}
```

## get user recipes favorite

- HTTP request: `GET user/favorite`
- Return value

```javascript
 {
    Favorite[]
 }
```

where

```javascript
  Favorite =
  {
    integer id,
    string added_date,
    int user,
    Recipe recipe
  }
```

where

```javascript
Recipe =
{
  integer id,
  string title,
  string? recipe_url,
  string? image_url,
  integer? cook_minute,
  integer? num_servings,
  string language,
  integer? num_ingredients
}
```

- Example

```json
{
    [
        {
            "id": 1,
            "added_date": "2022-12-08T21:17:46.953167+09:00",
            "user": 39,
            "recipe": {
                "id": 67379,
                "title": "recipe 1",
                "recipe_url": "",
                "image_url": "",
                "cook_minute": null,
                "num_servings": null,
                "language": "en",
                "num_ingredients": null
            }
        }
    ]
}
```

## add user recipe to favorites

- HTTP request: `POST user/favorite`
- Arguments

  - `integer recipe_id`

- Return value
  The new inserted favorite element

## delete user recipe from favorites

- HTTP request: `DELETE user/favorite`
- Arguments

  - `integer user_recipe_favorite_id`

- Return value

```javascript
{
    string message,
    integer deleted // the number of deleted items (should be 1)
}
```
