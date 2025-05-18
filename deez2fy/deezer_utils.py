from typing import List, Dict, Tuple

def extract_songs_artists(json_data: Dict) -> List[Tuple[str, str]]:
    """Extracts a list of tuples containing song names and artist names from a JSON object.
    """
    tracks = json_data.get("tracks", {}).get("data", [])
    songs_artists_tuples = [(track["title"], track["artist"]["name"]) for track in tracks]
    return songs_artists_tuples
