from spotipy import SpotifyOAuth, Spotify
from googlesearch import search
from typing import Dict, List

REDIRECT_URI = "http://127.0.0.1:8080"

class FindError(Exception):
    """Exception raised when a Spotify link / object has not been found."""
    pass


def auth(client_id: str, client_secret: str) -> Spotify:
    scope = "playlist-modify-public"
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
    spoti_client = Spotify(auth_manager=auth_manager)
    return spoti_client


def find(artist: str, song_name: str) -> str:
    """
    Finds the Spotify link of a song given its artist and name.

    Parameters:
    artist (str): The artist of the song.
    song_name (str): The name of the song.

    Returns:
    str: The Spotify link of the song.

    Raises:
    FindError: If the Spotify link was not found.
    """
    query = f"spotify.com/track/ {artist} {song_name}"
    final = None

    try:
        for url in search(query, stop=3):
            if "spotify.com/track" in url:
                final = url
                break
            elif "spotify.link" in url:  # if no direct link was found
                # perform additional search to find direct link
                for sub_url in search(url, stop=1):
                    if "spotify.com/track" in sub_url:
                        final = sub_url
                        break
        if final is None:
            raise FindError("Spotify link not found")
    except Exception as e:
        raise FindError(f"Error during the Spotify link research : {str(e)}")

    return final


def check_playlist(spotify: Spotify, playlist_name: str) -> str:
    """
    Checks if a playlist exists in the current user's library.

    Parameters:
    spotify (Spotify): A Spotify client instance used for interacting with Spotify's API.
    playlist_name (str): The name of the playlist to search for.

    Returns:
    str: The ID of the playlist if it exists

    Raises:
    FindError: If the playlist was not found.
    """
    names = spotify.current_user_playlists()["items"]
    for key in names:
        if playlist_name in key["name"]:
            return key["id"]
    raise FindError("Playlist not found")


def check_song(artist: str, song: str, track_id: str, spotify: Spotify) -> bool:
    """
    Checks if a Spotify track's name and artist match the given song name and artist.

    Parameters:
    artist (str): The artist to check.
    song (str): The song name to check.
    track_id (str): The Spotify ID of the track.
    spotify (Spotify): A Spotify client instance used for interacting with Spotify's API.

    Returns:
    bool: True if the artist and song match, False otherwise.
    """
    track = spotify.track(track_id, market="US")
    artists = extract_artists(track["artists"])
    return track["name"].lower() == song.lower() and artist.lower() in artists 


def extract_artists(artist_dicts: List[Dict]) -> List[str]:
    """
    Extracts a list of artist names from a list of Spotify artist dicts.

    Parameters:
    artist_dicts (list): A list of Spotify artist dicts.

    Returns:
    list: A list of artist names in lowercase.
    """
    return [artist["name"].lower() for artist in artist_dicts]
