from time import sleep
import spotify_utils as spo
import deezer_utils as deez
from utils import fetch_json_from_url, progress_print
import argparse
from dotenv import load_dotenv
import os
from loguru import logger


def main():
    # Args management
    parser = argparse.ArgumentParser(description="Converts a playlist from Deezer to Spotify")
    parser.add_argument(
        "-i",
        "--id",
        help="Deezer playlist ID (found in the URL when you open your playlist)",
        required=True,
    )
    parser.add_argument(
        "-n", "--name", help="Name of the playlist to create on Spotify", required=True
    )
    args = parser.parse_args()

    deezer_playlist_uri = "https://api.deezer.com/playlist/" + args.id
    playlist_name = args.name

    # Spotify authentication
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    spoti_client = spo.auth(client_id, client_secret)
    spoti_id = spoti_client.me()["id"]
    spoti_client.user_playlist_create(spoti_id, playlist_name)

    # Retrieve deezer playlist data
    json_data = fetch_json_from_url(deezer_playlist_uri)
    titles_and_artists = deez.extract_songs_artists(json_data)
    nb_songs = len(titles_and_artists)

    # Convert playlist
    print(f'Converting playlist "{playlist_name}" with {nb_songs} songs from Deezer to Spotify...')
    for idx, (song, artist) in enumerate(titles_and_artists):
        try:
            song_link = spo.find(artist=artist, song_name=song)
            playlist_id = spo.check_playlist(spoti_client, playlist_name)
            if spo.check_song(artist, song, song_link, spoti_client):
                spoti_client.playlist_add_items(playlist_id, [song_link])
                progress_print(idx, nb_songs, song, artist, is_ok=True)
            else:
                raise ValueError("Artist or title mismatch while retrieving song")

        except Exception as e:
            logger.debug(f"Error while converting {song} by {artist} : {e}")
            progress_print(idx, nb_songs, song, artist, is_ok=False)

        finally:
            sleep(1)  # rate limit


if __name__ == "__main__":
    main()
