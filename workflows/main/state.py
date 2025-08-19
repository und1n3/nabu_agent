from typing_extensions import TypedDict

from utils.schemas import QuestionType, SpotifyType


class MainGraphState(TypedDict):
    input_command: str
    question_type: QuestionType
    spotify_command: SpotifyType
    album: str
    song: str
    playlist: str
    radio: str
    web_search: str
    final_answer: str  # sentence to return
    final_answer_catala: str
