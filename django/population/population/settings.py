# Scrapy settings for population population
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os

import django

# The following two lines are added to use Django outside of manage.py context
# (interested in reusing Django model definitions for scrapy items)
os.environ["DJANGO_SETTINGS_MODULE"] = "refrigerator_catalogue.settings"
django.setup()

BOT_NAME = "population"

SPIDER_MODULES = ["population.spiders"]
NEWSPIDER_MODULE = "population.spiders"

EDAMAM_APPID = os.environ["SCRAPY_EDAMAM_APPID"]
EDAMAM_APPKEY = os.environ["SCRAPY_EDAMAM_APPKEY"]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'population (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and dos
DOWNLOAD_DELAY = int(os.environ["SCRAPY_DOWNLOAD_DELAY"])
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.environ["SCRAPY_CONCURRENT_REQ"])
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# For DepthMiddleware: https://github.com/scrapy/scrapy/blob/master/docs/topics/spider-middleware.rst#depthmiddleware
DEPTH_LIMIT = int(os.environ["SCRAPY_DEPTH_LIMIT"])

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "scrapy.spidermiddlewares.depth.DepthMiddleware": 300,
    # 'population.middlewares.PopulationSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'population.middlewares.PopulationDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "scrapy.extensions.throttle.AutoThrottle": None,
    "scrapy_domain_delay.extensions.CustomDelayThrottle": 300,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "population.pipelines.PopulationPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = os.environ["SCRAPY_USE_AUTOTHROTTLE"] == "True"
# The initial download delay
AUTOTHROTTLE_START_DELAY = int(os.environ["SCRAPY_DOWNLOAD_DELAY"])
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = float(os.environ["SCRAPY_TARGET_CONCURRENCY"])
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [429]
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
HTTPCACHE_STORAGE = "population.lib.storage.QueryFSCacheStorage"
HTTPCACHE_QUERIES = ["app_key", "app_id"]

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Allow recursive request to Edamam using ingredient names
EDAMAM_RECURSION = os.environ["SCRAPY_EDAMAM_RECURSION"] == "True"

# Set up custom delays per domain (Scrapy-Domain-Delay)
DOMAIN_DELAYS = {
    "edamam": float(
        os.environ.get("SCRAPY_EDAMAM_DELAY", str(6 * AUTOTHROTTLE_TARGET_CONCURRENCY))
    ),
}
