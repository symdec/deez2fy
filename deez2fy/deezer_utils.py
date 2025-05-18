from typing import List, Dict, Tuple

from loguru import logger
from .utils import fetch_json_from_url

LIMIT_TRACKS_PER_CALL = 500
DEEZER_PLAYLIST_URI = f"https://api.deezer.com/playlist/[ID]/tracks?limit={LIMIT_TRACKS_PER_CALL}"

def get_songs_artists(playlist_id: str) -> List[Tuple[str, str]]:
    """Retrieve songs and artists from a Deezer playlist.

    :param playlist_id: the ID of the Deezer playlist.
    :return: a list of tuples containing song names and artist names.
    :raises Exception: If an error occurs while retrieving the songs and artists.
    """
    try:
        url = DEEZER_PLAYLIST_URI.replace("[ID]", playlist_id)
        songs_and_artists: List[Tuple[str, str]] = []
        json_data = fetch_json_from_url(url)
        songs_and_artists.extend(extract_songs_artists(json_data))

        while "next" in json_data:
            next_uri = json_data["next"]
            json_data = fetch_json_from_url(next_uri)
            songs_and_artists.extend(extract_songs_artists(json_data))
        return songs_and_artists

    except Exception as e:
        logger.error(f"Error getting deezer songs and artists: {e}")
        raise e

    

def extract_songs_artists(json_data: Dict) -> List[Tuple[str, str]]:
    """Extracts a list of tuples containing song names and artist names from a JSON object dictionary.
    """
    tracks = json_data.get("data", [])
    songs_artists_tuples = [(track["title"], track["artist"]["name"]) for track in tracks]
    return songs_artists_tuples
