from workflows.main.state import MainGraphState
from tools.agents import execute_classifier_agent
from utils.schemas import QuestionType

from langchain_community.tools import DuckDuckGoSearchRun

import json
import logging

logger = logging.getLogger(__name__)


def enroute_question(state: MainGraphState) -> MainGraphState:
    logger.info("--- Enroute Question Node ---")
    pre_established_commands = json.load(open("data/prestablished_commands.json"))
    result: QuestionType = execute_classifier_agent(
        text=state["input_command"],
        preestablished_commands_schema=pre_established_commands,
    )
    state["question_type"] = result
    logger.info(f"Enrouting to: {result}")
    return state


def pre_established_commands(state: MainGraphState) -> MainGraphState:
    logger.info("--- Pre-Established Commands Node ---")

    return state


def internet_search(state: MainGraphState) -> MainGraphState:
    logger.info("--- Internet Search Node ---")

    search = DuckDuckGoSearchRun()
    # prepare the command in english
    # - calling agent to translate and prepare the search query

    query_text = ...
    search.invoke(query_text)

    # - call agent to translate back to catalan

    return state


def finish_action(state: MainGraphState) -> MainGraphState:
    logger.info("--- Final Action Node ---")

    return state
