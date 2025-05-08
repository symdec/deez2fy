import requests
from typing import Dict

PROGRESS_PRINT_LINE_LENGTH = 70

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
    status = "OK" if is_ok else "NOK"
    line_start = f"({index + 1}/{nb_songs}) [{song}] by [{artist}] :"
    line = line_start.ljust(PROGRESS_PRINT_LINE_LENGTH - 2, '.') + status
    print(line)

