from requests import Session
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import RequestException

from weather.config import (
    REQUEST_TIMEOUT,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_FORCELIST,
    RETRY_TOTAL,
)


def get(url: str) -> str:
    retries = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST,
    )

    with Session() as session:
        session.mount(url, adapter=HTTPAdapter(max_retries=retries))

        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except RequestException as error:
            raise RuntimeError('Request failed.') from error

        if 'html' not in response.headers['content-type']:
            raise RuntimeError("Content type isn't HTML.")

        return response.text
