import sys
from time import sleep
import deez2fy.spotify_utils as spo
import deez2fy.deezer_utils as deez
from deez2fy.utils import progress_print
import argparse
from dotenv import load_dotenv
import os
from loguru import logger

SLEEP_TIME = 2  # time to wait between requests (to minimize the risk of exceeding the rate limit)


def main():
    args = parse_args()

    # set logging level
    logger.remove()
    if args.debug:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")

    deezer_playlist_id = args.playlist_id
    playlist_name = args.playlist_name

    # Spotify authentication
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    spoti_client = spo.authenticate(client_id, client_secret)
    spoti_id = spoti_client.me()["id"]
    spoti_client.user_playlist_create(spoti_id, playlist_name)

    # retrieve song-artist tuples from Deezer playlist
    songs_and_artists = deez.get_songs_artists(deezer_playlist_id)
    nb_songs = len(songs_and_artists)
    failed_to_migrate_songs = []

    # convert playlist
    print(
        f'Converting playlist "{playlist_name}" with {nb_songs} songs from Deezer to Spotify...'
    )
    for idx, (song, artist) in enumerate(songs_and_artists):
        try:
            track_id_candidates = spo.search_track(
                spoti_client, artist=artist, song_name=song
            )
            if len(track_id_candidates) == 0:
                raise ValueError("Track not found on Spotify")

            playlist_id = spo.get_playlist_id(spoti_client, playlist_name)
            track_has_matched = False
            for track_id_candidate in track_id_candidates:
                if spo.check_song(artist, song, track_id_candidate, spoti_client):
                    track_has_matched = True
                    spoti_client.playlist_add_items(playlist_id, [track_id_candidate])
                    progress_print(idx, nb_songs, song, artist, is_ok=True)
                    break
            if not track_has_matched:
                raise ValueError("Artist or title mismatch between Deezer and Spotify")

        except Exception as e:
            logger.info(f"Error while converting {song} by {artist} : {e}")
            failed_to_migrate_songs.append((song, artist))
            progress_print(idx, nb_songs, song, artist, is_ok=False)

        finally:
            sleep(SLEEP_TIME)  # sleep time to avoid exceeding the rate limit

    # summary print
    if len(failed_to_migrate_songs) > 0:
        print(
            f"\nFailed to migrate the following songs (count: {len(failed_to_migrate_songs)}/{nb_songs}):"
        )
        for song, artist in failed_to_migrate_songs:
            print(f"  - [{song}] by [{artist}]")
    else:
        print("\nAll songs migrated successfully!")


def parse_args():
    """Parse main arguments"""
    parser = argparse.ArgumentParser(
        description="Converts a playlist from Deezer to Spotify"
    )
    parser.add_argument(
        "-i",
        "--id",
        dest="playlist_id",
        type=str,
        help="Deezer playlist ID (found in the URL of your playlist page)",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="playlist_name",
        type=str,
        help="Name of the playlist to create on Spotify",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="If set, debug logs will be displayed",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
