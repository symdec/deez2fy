from time import sleep
import urllib.error
import requests
import urllib
from typing import Dict
from loguru import logger

PROGRESS_PRINT_LINE_LENGTH = 70
RETRY_DELAY = 30
MAX_RETRY = 3
TOO_MANY_REQUEST_CODE = 429


def fetch_json_from_url(url: str) -> Dict:
    """
    Fetches JSON data from the given URL.

    Parameters:
    url (str): The URL of the JSON data.

    Returns:
    dict: The JSON data structure.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def progress_print(index: int, nb_songs: int, song: str, artist: str, is_ok: bool) -> None:
    """
    Prints a progress line with the index, total number of songs, song name, artist name and a status OK or NOK.

    Parameters:
    index (int): The index of the song.
    nb_songs (int): The total number of songs.
    song (str): The name of the song.
    artist (str): The name of the artist.
    is_ok (bool): Whether the conversion was successful or not.
    """
    status = "OK" if is_ok else "NOK"
    line_start = f"({index + 1}/{nb_songs}) [{song}] by [{artist}] :"
    line = line_start.ljust(PROGRESS_PRINT_LINE_LENGTH - 2, ".") + status
    print(line)


def retry_on_429(func, max_retries=MAX_RETRY, retry_delay=RETRY_DELAY):
    """
    A decorator that retries a given function if it receives a 429 status code.

    This decorator is meant to be used when calling web APIs that may return a 429 status code (Too Many Requests) if the rate limit is exceeded.

    Parameters:
    func (function): The function to retry.
    max_retries (int): The number of times to retry the function.
    retry_delay (int): The time in seconds to wait before retrying.

    Returns:
    The result of the function call.
    """
    for attempt in range(max_retries):
        try:
            return func()
        
        except requests.HTTPError as e:
            if e.response.status_code == TOO_MANY_REQUEST_CODE:
                logger.debug(
                    f"Received 'too many requests' error code. Waiting {retry_delay} seconds before retrying..."
                )
                sleep(retry_delay)
            else:
                raise e
            
        except urllib.error.HTTPError as e:
            if e.code == TOO_MANY_REQUEST_CODE:
                logger.debug(
                    f"Received 'too many requests' error code. Waiting {retry_delay} seconds before retrying..."
                )
                sleep(retry_delay)
            else:
                raise e
            
    raise Exception("Max retries exceeded")
