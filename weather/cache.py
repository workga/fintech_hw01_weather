import pickle
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from weather.config import CACHE_FILENAME, CACHE_INTERVAL


def read_cache(filename: str, interval: timedelta):
    if not Path(filename).exists():
        return {}

    with open(filename, 'rb') as f:
        cached_results = pickle.load(f)

    return {
        k: v
        for k, v in cached_results.items()
        if datetime.now() - v['datetime'] < interval
    }


def write_cache(cached_results, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(cached_results, f)


def timed_cache(
    cached_args: list[str],
    filename: str = CACHE_FILENAME,
    interval: timedelta = CACHE_INTERVAL,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_results = read_cache(filename, interval)

            key = ','.join([str(kwargs.get(x, '')) for x in cached_args])
            if key in cached_results:
                result = cached_results[key]['result']
            else:
                # If this raises an exception, the cache will not be saved,
                # although it has been modified in read_cache().
                result = func(*args, **kwargs)

                cached_results[key] = {
                    'datetime': datetime.now(),
                    'result': result,
                }

            write_cache(cached_results, filename)
            return result

        return wrapper

    return decorator
