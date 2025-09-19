from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from workflows.main.state import MainGraphState
from workflows.spotify_agent import nodes as nodes
from utils.schemas import SpotifyType
from dotenv import load_dotenv

load_dotenv()


def decide_type(state: MainGraphState) -> SpotifyType:
    return state["spotify_command"].value


def build_spotify_workflow() -> CompiledStateGraph:
    workflow = StateGraph(MainGraphState)

    workflow.add_node("What to play?", nodes.decide_action)
    workflow.add_node("Search and play", nodes.search_and_play_music)

    workflow.set_entry_point("What to play?")
    workflow.add_edge("Search and play", END)
    workflow.add_edge("What to play?", "Search and play")

    return workflow.compile()


def execute_main_workflow(user_input: str) -> None: ...
