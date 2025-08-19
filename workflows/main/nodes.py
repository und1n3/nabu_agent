from workflows.main.state import MainGraphState
from tools.agents import (
    execute_classifier_agent,
    execute_party_sentence,
    execute_search_text,
    execute_translator,
)
from utils.schemas import Classifier, QuestionType, PartySentence


import json
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
pre_established_commands = json.load(open("data/preestablished_commands.json"))


def enroute_question(state: MainGraphState) -> MainGraphState:
    logger.info("--- Enroute Question Node ---")
    result: Classifier = execute_classifier_agent(
        text=state["input_command"],
        preestablished_commands_schema=pre_established_commands,
    )
    state["question_type"] = result.classification
    logger.info(f"Enrouting to: {result.classification}")
    logger.info(f"Thought process: {result.thought}")
    return state


def pre_established_commands(state: MainGraphState) -> MainGraphState:
    logger.info("--- Pre-Established Commands Node ---")
    result: PartySentence = execute_party_sentence(
        text=state["input_command"],
        preestablished_commands_schema=pre_established_commands,
    )
    logger.info(f"Command Used: {result.command_used}")
    state["final_answer"] = result.sentence
    return state


def internet_search(state: MainGraphState) -> MainGraphState:
    logger.info("--- Internet Search Node ---")

    text_english = execute_translator(
        text=state["input_command"],
        origin_language="Català",
        destination_language="English",
    )
    logger.info(
        f"Original text: {state['input_command']}, translated text: {text_english}"
    )
    search: str = execute_search_text(input_command=text_english)
    logger.info(f"Result from the web search: {search}")

    state["final_answer"] = search

    return state


def finish_action(state: MainGraphState) -> MainGraphState:
    logger.info("--- Final Action Node ---")
    logger.info("Translating the final answer to reproduce in the speakers.")
    logger.info(f"Sentence: {state['final_answer']}")
    result = execute_translator(
        text=state["final_answer"],
        origin_language="English",
        destination_language="Catalan",
    )
    state["final_answer_catala"] = result
    logger.info(f"Translated Sentence: {state['final_answer_catala']}")
    # TODO: Here we should send this text to Nabu
    return state
