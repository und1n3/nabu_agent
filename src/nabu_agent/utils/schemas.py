from enum import Enum

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    spotify = "Spotify Command"
    internet = "Internet Search"
    party = "Party Mode"
    homeassistant = "HA Command"


class SpotifyType(str, Enum):
    TRACK = "track"  # play a specific song / track
    ARTIST = "artist"  # play artist
    ALBUM = "album"  # play an artist’s album
    PLAYLIST = "playlist"  # play a playlist
    RADIO = "radio"  # play radio (artist or song radio)


class Summarizer(BaseModel):
    answer: str = Field(description="The summarized answer extracted from the text.")


class STT(BaseModel):
    original_language: str = Field(
        description="The language the input command is written in. Just one word."
    )
    translated_command: str = Field(
        description="The input command translated from the original language to the defined destination language. Be accurate. If there is a name or an artist in the command, do not translate it."
    )


class Translator(BaseModel):
    original_language: str = Field(
        description="The language the input command is written in. Just one word."
    )
    translated_command: str = Field(
        description="The input command translated from the original language to the defined destination language. Be accurate. If there is a name or an artist in the command, do not translate it."
    )


class Classifier(BaseModel):
    classification: QuestionType = Field(
        description="Classification of the command given into: internet (internet search), spotify (play music), party (one of the preestablished commands) or homeassistant (for example turn on the light)."
    )


class PartySentence(BaseModel):
    command_used: str = Field(
        default="Didn't use any command",
        description="Get the most appropiate command for the imput sentence given the preestablished_commands dictionary",
    )
    sentence: str = Field(
        default="I have no idea.",
        description="Think a witty answer given the command and schema to follow.",
    )


class SpotifyClassifier(BaseModel):
    classification: SpotifyType = Field(
        description="classify the user input into one of the spotify type categories. If radio mentioned put radio. if song put track. if its an artist put artist. if album put album."
    )
    key_word: str = Field(
        description="Key artist, track or playlist to search for in Spotify. Between 1 and 10 words all in one line",
        min_length=1,
        max_length=10,
    )
