from time import sleep
import spotify_utils as spo
import deezer_utils as deez
from utils import fetch_json_from_url, progress_print, retry_on_429
import argparse
from dotenv import load_dotenv
import os
from loguru import logger

SLEEP_TIME = 5 # time to wait between requests (to minimize the risk of exceeding the rate limit)


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
            song_link = retry_on_429(lambda: spo.find(artist=artist, song_name=song))
            playlist_id = spo.check_playlist(spoti_client, playlist_name)
            if spo.check_song(artist, song, song_link, spoti_client):
                # try to add the song to the playlist, in case of rate limit, retry
                retry_on_429(lambda: spoti_client.playlist_add_items(playlist_id, [song_link]))
                progress_print(idx, nb_songs, song, artist, is_ok=True)
            else:
                raise ValueError("Artist or title mismatch between Deezer and Spotify")

        except Exception as e:
            logger.debug(f"Error while converting {song} by {artist} : {e}")
            progress_print(idx, nb_songs, song, artist, is_ok=False)

        finally:
            sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
