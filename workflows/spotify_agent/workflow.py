from workflows.main.state import MainGraphState
from langgraph.graph.graph import CompiledGraph
from langgraph.graph import StateGraph


def build_main_workflow(initial_state: MainGraphState) -> CompiledGraph:
    workflow = StateGraph(MainGraphState)


def execute_main_workflow(user_input: str) -> None: ...
