from functools import wraps
from time import sleep
import urllib.error
import requests
import urllib
from typing import Dict
from loguru import logger

PROGRESS_PRINT_LINE_LENGTH = 70
TOO_MANY_REQUEST_CODE = 429
RETRY_DELAY = 30
MAX_RETRY = 2


def fetch_json_from_url(url: str) -> Dict:
    """Fetches a JSON object from a given URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def progress_print(index: int, nb_songs: int, song: str, artist: str, is_ok: bool) -> None:
    """Prints a progress message.
    """
    status = "OK" if is_ok else "NOK"
    line_start = f"({index + 1}/{nb_songs}) [{song}] by [{artist}] :"
    line = line_start.ljust(PROGRESS_PRINT_LINE_LENGTH - 2, ".") + status
    print(line)


def retry_on_429(func):
    """Decorator to retry a function on HTTP 429 (Too Many Requests) errors.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRY):
            try:
                return func(*args, **kwargs)
            
            except requests.HTTPError as e:
                if e.response.status_code == TOO_MANY_REQUEST_CODE:
                    logger.info(
                        f"Received 'too many requests' error code. Waiting {RETRY_DELAY} seconds before retrying..."
                    )
                    sleep(RETRY_DELAY)
                else:
                    raise e
                
            except urllib.error.HTTPError as e:
                if e.code == TOO_MANY_REQUEST_CODE:
                    logger.info(
                        f"Received 'too many requests' error code. Waiting {RETRY_DELAY} seconds before retrying..."
                    )
                    sleep(RETRY_DELAY)
                else:
                    raise e
        raise Exception("Max retries exceeded")
    return wrapper
