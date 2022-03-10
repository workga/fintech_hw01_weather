from datetime import timedelta

BASE_URL = 'https://world-weather.ru/pogoda/russia/'

# http_requests
REQUEST_TIMEOUT = (1, 2)

RETRY_TOTAL = 5
RETRY_BACKOFF_FACTOR = 0.1
RETRY_STATUS_FORCELIST = [500, 502, 503, 504]

# parser
TAG_ID = 'weather-now-number'

# cache
CACHE_FILENAME = '.weather.cache'
CACHE_INTERVAL = timedelta(seconds=5)
