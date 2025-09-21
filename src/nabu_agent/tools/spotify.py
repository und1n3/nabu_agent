from typing import Optional

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from ..utils.schemas import SpotifyType

load_dotenv()

scope = [
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "user-library-read",
]

DEVICE_NAME = "librespot"
DEVICE_ID = "7c28ab8a5c9512e4266ac7cb756312c82ee43d7e"


spotify_client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, cache_path="/.cache")
)
print(spotify_client.devices())


def play_music(context_uri: Optional[str] = None, uris: Optional[str] = None) -> None:
    if context_uri:
        spotify_client.start_playback(device_id=DEVICE_ID, context_uri=context_uri)
    else:
        spotify_client.start_playback(device_id=DEVICE_ID, uris=[uris])


def search_music(criteria_type: SpotifyType, query: str):
    if criteria_type == SpotifyType.RADIO:
        criteria_type = "playlist"
        query = "this%20is%20" + query
    else:
        criteria_type = criteria_type.value

    print(f"______________ {criteria_type} ____ {query}")

    result = spotify_client.search(q=query, type=[criteria_type], limit=2)
    print(result[criteria_type + "s"]["items"])
    result_id = result[criteria_type + "s"]["items"][0]["uri"]
    print(result_id)
    return result_id
