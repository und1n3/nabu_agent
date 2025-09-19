from workflows.main.state import MainGraphState
from utils.schemas import SpotifyType, SpotifyClassifier
import logging
from dotenv import load_dotenv
from tools.agents import execute_spotify_classifier_agent
from tools.spotify import play_music, search_music

load_dotenv()

logger = logging.getLogger(__name__)


def decide_action(state: MainGraphState):
    logger.info("--- Decide Spotify Command Type Node ---")
    result: SpotifyClassifier = execute_spotify_classifier_agent(
        text=state["english_command"],
    )
    state["spotify_command"] = result.classification
    state["spotify_query"] = result.key_word.replace(" ", "%20")

    logger.info(f"Enrouting to: {result.classification}")
    logger.info(f"Query: {result.key_word}")
    return state


def search_and_play_music(state: MainGraphState) -> MainGraphState:
    logger.info("--- Search & Play Song Node ---")
    id = search_music(
        query=state["spotify_query"],
        criteria_type=state["spotify_command"],
    )
    if state["spotify_command"] == SpotifyType.TRACK:
        uris = id
        context_uri = None
    else:
        uris = None
        context_uri = id
    print(f"context_uri: {context_uri}, uris: {uris}")
    play_music(context_uri=context_uri, uris=uris)
    state["final_answer"] = f"Playing: {state['english_command']}"
    return state
