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


class Summarizer(BaseModel):
    answer: str = Field(description="The summarized answer extracted from the text.")


class Translator(BaseModel):
    original_language: str = Field(
        description="The language the input command is written in. Just one word."
    )
    translated_command: str = Field(
        description="The input command translated from the original language to the defined destination language. Be accurate."
    )


class Classifier(BaseModel):
    classification: QuestionType = Field(
        description="Classification of the command given into: internet (internet search), spotify (play music) or party (one of the preestablished commands)."
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
        description="Think thoroughly your answer, return  your thought process summarized."
    )
    classification: SpotifyType = Field(
        description="classify the user input into one of the spotify type categories"
    )
