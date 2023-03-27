# Refrigerator Catalogue API
For DB Population, please refer to [DB Population README](population/README.md).

## Directory Structure
```
.
├── README.md
├── example                 (example app)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations          (auto-generated)
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py               (main CLI)
├── population              (DB population scripts)
├── refrigerator_catalogue  (main project)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         (global settings)
│   ├── urls.py             (global routes config)
│   └── wsgi.py
└── requirements.txt
```

## Import DB from fixtures (`db.json`)
1. From the project root directory, run `docker compose -f docker/docker-compose.yml up --build -d` to start the env
2. Run `docker compose -f docker/docker-compose.yml exec django bash` to run `bash` inside the `django` container
3. (Optional) run `./manage.py dumpdata api -o db-backup.json` to create a current snapshot of your DB, just in case
    - If you get an error, you are most likely having nothing in your DB. In this case, you can safely continue to the next step
4. Run `./manage.py migrate` to create and update DB tables
5. Run `./manage.py shell` to start the Django shell
6. Run this command to clear the already-collected data, if any: `from api.models import *;Ingredient.objects.all().delete();Recipe.objects.all().delete();Tag.objects.all().delete();QuantityScaleUnit.objects.all().delete()`
    After this, please exit the Django shell
7. Run `./manage.py loaddata db.json` (this may take a few minutes depending on the size)
8. Run `docker compose -f docker/docker-compose.yml down -t 2` to stop the environment

## Export DB to JSON
Steps are as follows:
- From `django/` directory (of `django` container), run `./manage.py shell` to open up the Django shell
- Inside the Django shell, run the following two lines of code to generate `django/.db.json`
    - `from api.json import export`
    - `export()`
        - Instead, run `export(path="../docker/json-server/db.json", indent=3, override=True)` to override the json-server's DB

To customise the behavior, feel free to modify `django/api/json.py`. It should be simple to add other tables, for example.

__Note:__ After exporting, move the file to `docker/json-server` and rename to `db.json`. After that please rebuild your json-server container.

## Example App
An example app is configured in `example/` directory.  

### Usage
After starting the backend development environment, you have to apply DB migrations by running `python manage.py migrate` inside the `django` container (by using e.g., the integrated shell in VSCode Dev Containers).  
Then, you can visit `http://localhost:8000/example/product/` for the browser interface.

To work with the API using `curl`, try the following commands in the shell:
- GET /example/product/
    - `curl -X GET http://localhost:8000/example/product/`
        - This should return all the products in DB
- POST /example/product/
    - `curl -X POST http://localhost:8000/example/product/ -d "title=example product" -d "price=1000" -d "description=example product" -d "summary=example product"`
        - This should create a new product in Product table and returns the created product
