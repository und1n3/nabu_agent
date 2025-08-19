from utils.schemas import (
    QuestionType,
    Classifier,
    PartySentence,
    SpotifyClassifier,
    SpotifyType,
)
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import logging
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

load_dotenv()


def get_model() -> ChatOllama:
    model = ChatOllama(model="devstral", temperature=0.15, top_p=1 - 0.01, num_ctx=8192)
    # model = ChatOllama(model="llama3.2")

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
    llm = get_model()
    search_tool = DuckDuckGoSearchResults()
    tools = [
        Tool(
            name="Internet Search",
            func=search_tool.run,
            description="Useful for searching information on the internet. Use this when you need to find current or factual information.",
        )
    ]

    # Define the prompt template for the agent
    system = """
    You are an internet searcher. Look up the question asked using your tool.
    REturn just the answer.
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """User question: \n\n {input} """,
            ),
        ]
    )

    agent = answer_prompt | llm.bind_tools(tools)
    result = agent.invoke({"input": input_command})
    logger.info(f"Answer: {result.content}")
    return result.content


def execute_party_sentence(text, preestablished_commands_schema) -> PartySentence:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(PartySentence)

    system = """
    You must assess which prestablished command the given text matches the best.
    Then , following the command's description, return a witty answer .
    Think this is a party / joke mode.

    Every Command will start with ok, Nabu (or something similar), ignore this part of the text.
    The preestablished commands are in the format {{trigger_sentence : description of the type of answer you have to say}}
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

    party_model: RunnableSequence = answer_prompt | structured_llm_grader

    result: PartySentence = party_model.invoke(
        {
            "preestablished_commands_schema": preestablished_commands_schema,
            "text": text,
        }
    )
    return result


def execute_translator(text, origin_language, destination_language) -> str:
    llm = get_model()

    system = """
    You must accurately translate the given sentence from the origin language to the destination language. 
    Keep the connotations.
    
    Think thoroughly your answer, it should be in the requested format.
    ** Return ONLY the translated sentence**
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """
                - Text to translate: {text}
                - Origin Language : {origin_language}
                - Destination language: {destination_language}
                """,
            ),
        ]
    )

    party_model: RunnableSequence = answer_prompt | llm

    result: str = party_model.invoke(
        {
            "text": text,
            "origin_language": origin_language,
            "destination_language": destination_language,
        }
    )
    return result.content


def execute_spotify_classifier_agent(text) -> SpotifyType:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(SpotifyClassifier)

    system = """

    Instructions:
    - Translate the question into english.
    - Decide which of the given Spotify commands suits best [radio, song, playlist or album]
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """User command: \n\n {text} """,
            ),
        ]
    )

    classifier: RunnableSequence = answer_prompt | structured_llm_grader

    result: SpotifyClassifier = classifier.invoke(
        {
            "text": text,
        }
    )

    return result
