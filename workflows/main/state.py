from typing_extensions import TypedDict
from utils.schemas import QuestionType, SpotifyType


class MainGraphState(TypedDict):
    input_command: str
    question_type: QuestionType
    spotify_type: SpotifyType
    album: str
    song: str
    playlist: str
    radio: str
    web_search: str
