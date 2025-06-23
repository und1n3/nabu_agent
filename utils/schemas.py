from enum import Enum


class QuestionType(str, Enum):
    spotify = "Spotify Command"
    internet = "Internet Search"
    party = "Party Mode"


class SpotifyType(str, Enum):
    radio = "Spotify Radio"
    album = "Artist Album"
    playlist = "Playlist"
