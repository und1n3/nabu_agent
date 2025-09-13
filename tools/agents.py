from utils.schemas import (
    Summarizer,
    Translator,
    QuestionType,
    Classifier,
    PartySentence,
    SpotifyClassifier,
    SpotifyType,
)
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
import logging
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SearxSearchWrapper
import os
from tools.misc import search_and_fetch

logger = logging.getLogger(__name__)

load_dotenv()


def get_model() -> ChatOllama:
    # model = ChatOllama(
    #     model="qwen3:30b", temperature=0.15, top_p=1 - 0.01, num_ctx=8192
    # )
    # model = ChatOllama(model="llama3.2")
    model = ChatOpenAI(
        model="GPT-OSS-20B",
        # model="GPT-OSS-120B-Low-F16",
        api_key=os.environ["API_KEY"],
        base_url=os.environ["BASE_URL"],
    )
    return model


def execute_classifier_agent(
    english_command, preestablished_commands_schema
) -> QuestionType:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(Classifier)

    system = """
    You must assess if the given text is one of the prestablished commands, a question that needs internet access or a command to play music in spotify.
    The preestablished commands are in the format {{trigger_sentence : description of the type of answer you have to say}}
    
    **INSTRUCTIONS**:
    - Think thoroughly what time of command you are asked. it should fall within one of the given categories
    - Decide whether it should go for the spotify command (playing music), for a search result in the web (a question about general or up to date knowledge) or if it is found within the prestablished commands (given list)
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """- command:  {text}
                  - prestablished commands: {preestablished_commands_schema}
                  - Question categories: {question_categories}
                  """,
            ),
        ]
    )

    classifier: RunnableSequence = answer_prompt | structured_llm_grader

    result: Classifier = classifier.invoke(
        {
            "preestablished_commands_schema": preestablished_commands_schema,
            "text": english_command,
            "question_categories": QuestionType,
        }
    )
    return result


def execute_search_text(english_command):
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(Summarizer)
    search_result = search_and_fetch(
        query=english_command, num_results=2, chunk_size=1500
    )

    logger.info(f"\n\n Search Result: {search_result}")
    # Define the prompt template for the agent
    system = """
    You are an expert in summarizing content and giving the most accurate information. Given an initial command an the text containing the information,
    Give an answer to the command using the information provided in the text. Keep it short, around one sentence.
    
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """ Command: {command}
                    Text: \n\n {text} """,
            ),
        ]
    )

    agent = answer_prompt | structured_llm_grader
    result = agent.invoke({"command": english_command, "text": search_result})
    logger.info(f"Answer: {result.answer}")
    return result.answer


def execute_party_sentence(text, preestablished_commands_schema) -> PartySentence:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(PartySentence)

    system = """
    You must assess which prestablished command the given text matches the best.
    Then , following the command's description, return a witty answer .
    Think this is a party / joke mode.
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


def execute_translator(text: str, destination_language: str) -> Translator:
    llm = get_model()
    structured_llm_grader = llm.with_structured_output(Translator)

    system = """
    You are a language expert, you will be working mainly in catalan and english.Think thoroughly the meaning of the sentence and translate it to the best of your abilities. 
    Translate word by word the given text. Be aware of double meanings in words, choose the correct translation.

    **INSTRUCTIONS:**
    - Detect the language of the given sentence 
    - translate the text from the original language to the destination language. Return just the text translated.
    
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                """
                - Text to translate: {text}
                - Destination language: {destination_language}
                """,
            ),
        ]
    )
    traslator_llm: RunnableSequence = answer_prompt | structured_llm_grader

    result: Translator = traslator_llm.invoke(
        {
            "text": text,
            "destination_language": destination_language,
        }
    )
    return result


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
