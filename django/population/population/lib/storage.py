# QueryFSCacheStorage is FilesystemCacheStorage with custom query omitted

from scrapy import Request
from scrapy.extensions.httpcache import FilesystemCacheStorage
from scrapy.settings import Settings


class QueryFSCacheStorage(FilesystemCacheStorage):
    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.queries = settings.get("HTTPCACHE_QUERIES", [])

    def _get_request_path(self, spider, request: Request):
        """trim any query args if the key matches self.queries"""

        if "?" not in request.url:  # fallback
            return super()._get_request_path(spider, request)

        # drop queries that exist in self.queries
        queries = request.url.split("?")[1].split("&")
        filterred = []
        for query in queries:
            key = query.split("=")[0]
            if key in self.queries:
                continue  # skip
            filterred.append(query)

        # construct the new url from the filterred queries
        url = request.url.split("?")[0] + "?" + "&".join(filterred)

        # update the request object with the new url
        request = request.replace(url=url)

        return super()._get_request_path(spider, request)
