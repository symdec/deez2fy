# Deez2fy : Deezer to Spotify playlist converter

This project allows to migrate your Deezer playlists to Spotify.

## Install

### Using uv
This project was built using *uv* as Python dependencies manager, which is fast and precisely tracks the dependencies.  
You can install uv very quickly here : https://docs.astral.sh/uv/getting-started/installation/.

Run this command to install the dependencies in your uv project environment :
```
$ uv sync
```

### Using pip
If so, it is recommended to use a virtual environment to install the dependencies.  

Pip-install the dependencies listed in `pyproject.toml`.  
Ex :   
```
$ pip install \
    deezer-python \
    google \
    loguru \
    python-dotenv \
    spotipy
```

Exact info on versions can be found in the `pyproject.toml`. 


## Getting started

Once your Python environment is ready, to migrate a Deezer playlist to Spotify :

1. Make the Deezer playlist public

2. Go to your playlist in the web and retrieve its ID in the URL (e.g.: `1306085715`)

3. Create / Connect to your Spotify dev account, going here https://developer.spotify.com/dashboard 

4. In your Spotify dev dashboard, create a project (named "Deezer migration" for example)

5. Set the redirect URI to the value `http://127.0.0.1:8080`

6. In your Spotify project, retrieve your **Client ID** and **Client Secret**.

7. Back to this git project, on the root, create a `.env` file containing your Spotify API credentials, like below :
```
SPOTIFY_CLIENT_ID=<ID>
SPOTIFY_CLIENT_SECRET=<SECRET>
```
Where `<ID>` is the client ID and `<SECRET>` the client secret you retrieved.

8. Run the main file :  

**Case 1 : Using uv**  
Run `uv run main.py -i <DEEZER_PLAYLIST_ID> -n <PLAYLIST_NAME_ON_SPOTIFY>`  

Ex : `uv run main.py -i 1306085715 -n "My Playlist"`

**Case 2 : Using pip**

Run `python main.py -i <DEEZER_PLAYLIST_ID> -n <PLAYLIST_NAME_ON_SPOTIFY>`

Ex : `python main.py -i 1306085715 -n "My Playlist"`


> More help on usage can be seen using the option `--help` / `-h`

## Known issues (for future improvements)

- If the Deezer playlist has more than 400 tracks, only the first 400 will be migrated
- Some tracks that exist on Spotify are not migrated properly (not found during the search) 