from workflows.main.state import MainGraphState
from utils.schemas import SpotifyType
import logging
from dotenv import load_dotenv
from tools.agents import execute_spotify_classifier_agent

load_dotenv()

logger = logging.getLogger(__name__)


def decide_action(state: MainGraphState):
    logger.info("--- Decide Spotify Command Typpe Node ---")
    result: SpotifyType = execute_spotify_classifier_agent(
        text=state["english_command"],
    )
    state["spotify_command"] = result.classification
    logger.info(f"Enrouting to: {result.classification}")
    logger.info(f"Thought process: {result.thought}")
    return state


def play_song(state: MainGraphState):
    logger.info("--- Play Song Node ---")
    state["final_answer"] = "Done"
    # TODO: Link with the functionality to play a song in NABU
    return state


def play_playlist(state: MainGraphState):
    logger.info("--- Play Playlist Node ---")
    state["final_answer"] = "Done"
    # TODO: Link with the functionality to play a song in NABU

    return state


def play_album(state: MainGraphState):
    logger.info("--- Play Album Node ---")
    state["final_answer"] = "Done"
    # TODO: Link with the functionality to play a song in NABU

    return state


def play_radio(state: MainGraphState):
    logger.info("--- Play Radio Node ---")
    state["final_answer"] = "Done"
    # TODO: Link with the functionality to play a song in NABU

    return state
