from utils.schemas import QuestionType, SpotifyType, Classifier
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import logging

logger = logging.getLogger(__name__)


def get_model() -> ChatOllama:
    model = ChatOllama(model="devstral")
    return model


def execute_classifier_agent(text, preestablished_commands_schema) -> QuestionType:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(Classifier)

    system = """
    You must assess if the given text is a prestablished command, a question that needs internet access or a command to play music in spotify.
    Every Command will start with ok, Nabu (or something similar)
    The preestablished commands are in the format {{trigger_sentence : description of the type of answer you have to say}}
    Instructions:
    - Translate the question into english.
    - Decide whether it should go for the spotify command, for a search result in the web or if it is found within the prestablished commands
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """User question: \n\n {text} \n\n prestablished commands: {preestablished_commands_schema}""",
            ),
        ]
    )

    classifier: RunnableSequence = answer_prompt | structured_llm_grader

    result: Classifier = classifier.invoke(
        {
            "preestablished_commands_schema": preestablished_commands_schema,
            "text": text,
        }
    )
    return result


def execute_search_text(input_command):
    # prepare the text
    llm = get_model()

    system = """ You must assess if the given text is a prestablished command, a question that needs internet access or a command to play in spotify."""

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "User question: \n\n {input_command} ",
            ),
        ]
    )

    classifier: RunnableSequence = answer_prompt | llm

    result: QuestionType = classifier.invoke(
        {
            "input_command": input_command,
        }
    )
    return result.content


def execute_translator(text, origin_language, destination_language): ...
