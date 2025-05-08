# Deez2fy : Deezer to Spotify playlist converter

This project allows to migrate your Deezer playlists to Spotify.

## Install

### Using uv
This project was built using *uv* as Python dependencies manager, which is fast and precisely tracks the dependencies.  
You can install uv very quickly here : https://docs.astral.sh/uv/getting-started/installation/.


TODO

### Using pip
If so, it is recommended to use a virtual environment to install the dependencies.  

Pip-install the dependencies listed in `pyproject.toml`.  
Ex :   
```
pip install \
    deezer-python \
    google \
    loguru \
    python-dotenv \
    spotipy
```

Exact info on versions can be found in the `pyproject.toml`. 


## Getting started

Once your Python environment is ready,

TODO playlist must be public
TODO details on spotify API
TODO redirect URI info

In the root of this project, create a `.env` file containing your Spotify API credentials, like below :
```
SPOTIFY_CLIENT_ID=<ID>
SPOTIFY_CLIENT_SECRET=<SECRET>
```
Where `<ID>` is your Spotify API app ID and `<SECRET>` your Spotify API app secret.


TODO usage
