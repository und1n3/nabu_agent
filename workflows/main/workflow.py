from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph

from utils.schemas import QuestionType
from workflows.main import nodes as nodes
from workflows.main.state import MainGraphState
from workflows.spotify_agent.workflow import (
    build_spotify_workflow,
)

from dotenv import load_dotenv

load_dotenv()


def decide_action(state: MainGraphState) -> QuestionType:
    if "question_type" in state:
        return state["question_type"].value
    return END


def build_main_workflow() -> CompiledGraph:
    workflow = StateGraph(MainGraphState)
    workflow.add_node("Enrouting Question", nodes.enroute_question)
    workflow.add_node("Pre-stablished commands", nodes.pre_established_commands)
    workflow.add_node("Internet search", nodes.internet_search)
    workflow.add_node("Spotify Command", build_spotify_workflow())
    workflow.add_node("Finish Action", nodes.finish_action)

    workflow.add_conditional_edges(
        "Enrouting Question",
        decide_action,
        {
            QuestionType.internet.value: "Internet search",
            QuestionType.party.value: "Pre-stablished commands",
            QuestionType.spotify.value: "Spotify Command",
            END: END,
        },
    )
    workflow.set_entry_point("Enrouting Question")
    workflow.add_edge("Pre-stablished commands", "Finish Action")
    workflow.add_edge("Internet search", "Finish Action")
    workflow.add_edge("Spotify Command", "Finish Action")
    workflow.set_finish_point("Finish Action")
    return workflow.compile()


def execute_main_workflow(user_input: str) -> None:
    app = build_main_workflow()
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")
    app.get_graph(xray=1).draw_mermaid_png(output_file_path="full_graph.png")
    app.invoke({"input_command": user_input})
