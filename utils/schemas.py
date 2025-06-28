from enum import Enum
from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    spotify = "Spotify Command"
    internet = "Internet Search"
    party = "Party Mode"


class SpotifyType(str, Enum):
    radio = "Play Spotify Radio"
    album = "Play Artist Album"
    playlist = "Play Playlist"
    song = "Play Song"


class Classifier(BaseModel):
    thought: str = Field(
        description="Think through your answer, return  your thought process summarized."
    )
    classification: QuestionType = Field(
        description="classify the user input into one of the question type categories"
    )
