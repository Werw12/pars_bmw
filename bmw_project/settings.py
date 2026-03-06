BOT_NAME = "bmw_project"

SPIDER_MODULES = ["bmw_project.spiders"]
NEWSPIDER_MODULE = "bmw_project.spiders"

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 30

RETRY_ENABLED = True
RETRY_TIMES = 3

DEFAULT_REQUEST_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.9",
    "origin": "https://usedcars.bmw.co.uk",
    "referer": "https://usedcars.bmw.co.uk/",
}

DOWNLOADER_MIDDLEWARES = {
    "bmw_project.middlewares.RandomUserAgentMiddleware": 543,
}

ITEM_PIPELINES = {
    "bmw_project.pipelines.DataValidationPipeline": 100,
    "bmw_project.pipelines.AsyncSQLitePipeline": 300,
}

LOG_LEVEL = "DEBUG"
