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
    thought: str = Field(
        description="Think through your answer, return  your thought process summarized."
    )
    classification: SpotifyType = Field(
        description="classify the user input into one of the question type categories"
    )
