import json

from tools.agents import execute_classifier_agent
from utils.schemas import Classifier, QuestionType

preestablished_commands_schema = json.load(open("data/preestablished_commands.json"))


def test_classifier_agent_internet_1():
    input_prompt = "Quin temps fa avui a mataró?"
    result: Classifier = execute_classifier_agent(
        text=input_prompt, preestablished_commands_schema=preestablished_commands_schema
    )
    assert result.classification == QuestionType.internet


def test_classifier_agent_internet_2():
    input_prompt = "quin any va ser la revolució francesa?"
    result: Classifier = execute_classifier_agent(
        text=input_prompt, preestablished_commands_schema=preestablished_commands_schema
    )
    assert result.classification == QuestionType.internet


def test_classifer_agent_spotify_1():
    input_prompt = "Posa una cançó de Mika"
    result: Classifier = execute_classifier_agent(
        text=input_prompt, preestablished_commands_schema=preestablished_commands_schema
    )
    assert result.classification == QuestionType.spotify


def test_classifer_agent_party_1():
    input_prompt = "boom"
    result: Classifier = execute_classifier_agent(
        text=input_prompt, preestablished_commands_schema=preestablished_commands_schema
    )
    assert result.classification == QuestionType.party
