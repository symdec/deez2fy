from typing import List, Dict, Tuple

def extract_songs_artists(json_data: Dict) -> List[Tuple[str, str]]:
    """
    Extracts a list of tuples of song title and artist name from Deezer JSON structure.

    Parameters:
    json_data (dict): The JSON data structure containing the tracks.

    Returns:
    list[tuple[str, str]]: A list of tuples of song title and artist name.
    """
    tracks = json_data.get("tracks", {}).get("data", [])
    songs_artists_tuples = [(track["title"], track["artist"]["name"]) for track in tracks]
    return songs_artists_tuples
