from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph

from workflows.main.state import MainGraphState
from workflows.spotify_agent import nodes as nodes
from utils.schemas import SpotifyType


def decide_type(state: MainGraphState) -> SpotifyType:
    return state["spotify_type"].value


def build_spotify_workflow() -> CompiledGraph:
    workflow = StateGraph(MainGraphState)

    workflow.add_node("What to play?", nodes.decide_action)
    workflow.add_node(SpotifyType.song.value, nodes.play_song)
    workflow.add_node(SpotifyType.playlist.value, nodes.play_playlist)
    workflow.add_node(SpotifyType.album.value, nodes.play_album)
    workflow.add_node(SpotifyType.radio.value, nodes.play_radio)

    workflow.add_conditional_edges(
        "What to play?",
        decide_type,
        {
            SpotifyType.album.value: SpotifyType.album.value,
            SpotifyType.song.value: SpotifyType.song.value,
            SpotifyType.radio.value: SpotifyType.radio.value,
            SpotifyType.playlist.value: SpotifyType.playlist.value,
        },
    )
    workflow.set_entry_point("What to play?")
    workflow.add_edge(SpotifyType.album.value, END)
    workflow.add_edge(SpotifyType.song.value, END)
    workflow.add_edge(SpotifyType.radio.value, END)
    workflow.add_edge(SpotifyType.playlist.value, END)
    return workflow.compile()


def execute_main_workflow(user_input: str) -> None: ...
