# DB Population

## Directory Structure
```
.
├── README.md
├── .scrapy/              (cache-store for previous requests)
├── population
│   ├── __init__.py
│   ├── items.py          (def of items passed from spider to pipeline)
│   ├── middlewares.py
│   ├── pipelines.py      (save items to DB)
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── api_spider.py (crawl APIs and yield items)
└── scrapy.cfg
```

## Debug
From the project root directory, run `cp .vscode/launch.json .vscode/launch.json.example`.  
After this, you can use `RUN AND DEBUG` feature of VSCode to launch Scrapy in the debug mode.  

## Usage
### One liner
`docker compose -f docker/docker-compose.yml up django --build -d && time docker compose -f docker/docker-compose.yml exec django bash -c "./manage.py migrate && cd population && scrapy crawl api_spider -L WARNING -a letter=a-z" && docker compose -f docker/docker-compose.yml down -t 2`

### Manual
Inside the `django` container, go to `django/population/` directory and run `scrapy crawl api_spider -L WARNING -a letter=a`.
This command runs our spider (`api_spider`) with the keyword argument `letter=a` (`-a` is for `argument`).  

The `letter` keyword argument is used for obtaining an initial list of recipe titles that is used for the following recursive scraping over Edamam API.  
If you set `letter=a`, the scrapy obtains the initial recipe titles that start with `'a'`.  
You can also set a range (inclusive) like this: `letter=a-c`.  

`-L` argument specifies the log level. All the available log levels are listed in their [doc](https://docs.scrapy.org/en/latest/topics/logging.html#log-levels).  

If this fails with errors, you might have not applied migrations. Go to `django/` directory and run `./manage.py migrate` for this.

You can overwrite environment variables used in Scrapy by listing them before `scrapy` command like this:
`SCRAPY_USE_AUTOTHROTTLE=False SCRAPY_DOWNLOAD_DELAY=2 SCRAPY_CONCURRENT_REQ=4 SCRAPY_DEPTH_LIMIT=8 scrapy crawl api_spider -a letter=a -L DEBUG`

## Development
Please select the `django` container when starting Dev Containers.  

You can optionally create `.env` file in `docker/` directory (relative to the project root) to override some environment variables.  
For example, if you write `SCRAPY_DOWNLOAD_DELAY=5` in that file, `docker-compose.yml` respects this value and discard the default value, `3` defined in `docker-compose.yml`.

### Clearing DB for Development
You might want to clear your DB while developing features for the DB population.
In order to do that, you should (from the Django Dev Container terminal):
1. Run `python manage.py sqlflush` (in `/app/django` folder). This will **output several commands** to run. 
2. Copy the output (commands).
3. Open up the terminal inside the postgres container, run `psql` command to log into the postgres interactive mode.
4. Paste the commands.
5. (You might need to add `CASCADE` at the end of the `TRUNCATE` line before `;`).
6. **Run the commands**.

It should look like something:
```sql
BEGIN;
TRUNCATE "api_useringredient", ... RESTART IDENTITY;
COMMIT;
```
