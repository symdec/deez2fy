from spotipy import SpotifyOAuth, Spotify
from typing import Dict, List
from .utils import retry_on_429
from loguru import logger

REDIRECT_URI = "http://127.0.0.1:8080"


class FindError(Exception):
    """Exception raised when a Spotify link / object has not been found."""

    pass


def authenticate(client_id: str, client_secret: str) -> Spotify:
    """Authenticates with Spotify and returns a Spotify client instance."""
    scope = "playlist-modify-public"
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
    spoti_client = Spotify(auth_manager=auth_manager)
    return spoti_client


@retry_on_429
def search_track(spotify: Spotify, artist: str, song_name: str) -> str:
    """Search a Spotify track by artist and song name

    :param spotify: a Spotify client instance used for interacting with Spotify's API.
    :param artist: the artist name
    :param song_name: the song name
    :return: the first result of the search
    """
    result = spotify.search(
        q=f"artist:{artist} track:{song_name}", limit=1, type="track"
    )
    track_id = result["tracks"]["items"][0]["id"]
    name = result["tracks"]["items"][0]["name"]
    artists = result["tracks"]["items"][0]["artists"]
    logger.debug(
        f'Found track: {name} by {", ".join([artist["name"] for artist in artists])}'
    )
    return track_id


@retry_on_429
def get_playlist_id(spotify: Spotify, playlist_name: str) -> str:
    """
    Get the ID of a playlist by name

    :param spotify: a Spotify client instance used for interacting with Spotify's API.
    :param playlist_name: the name of the playlist to search for.
    :return: the ID of the playlist if it exists
    :raises FindError: if the playlist was not found.
    """
    names = spotify.current_user_playlists()["items"]
    for key in names:
        if playlist_name in key["name"]:
            return key["id"]
    raise FindError("Playlist not found")


@retry_on_429
def check_song(artist: str, song: str, track_id: str, spotify: Spotify) -> bool:
    """Check if a Spotify track's name and artist match the given song name and artist.

    :param artist: The artist to check.
    :param song: The song name to check.
    :param track_id: The Spotify ID of the track.
    :param spotify: A Spotify client instance used for interacting with Spotify's API.
    :return: True if the artist and song match, False otherwise.
    """
    track = spotify.track(track_id, market="US")
    artists = extract_artists(track["artists"])
    return track["name"].lower() == song.lower() and artist.lower() in artists


def extract_artists(artist_dicts: List[Dict]) -> List[str]:
    """Extracts a list of artist names from a list of Spotify artist dicts.

    :param artist_dicts: A list of Spotify artist dicts.
    :return: A list of artist names in lowercase.
    """
    return [artist["name"].lower() for artist in artist_dicts]
