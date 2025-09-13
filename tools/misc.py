from langchain_community.utilities import SearxSearchWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import BrowserbaseLoader
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()


def search_and_fetch(query: str, num_results: int = 3, chunk_size: int = 500) -> str:
    # search via SearxNG
    searx = SearxSearchWrapper(searx_host=os.environ["SEARX_HOST"])
    results = searx.results(query, num_results=num_results)

    output_texts = []

    # fetch page content
    for i, r in enumerate(results):
        url = r["link"]
        print(url)
        try:
            loader = WebBaseLoader(web_path=url)
            docs = loader.lazy_load()
            content = ""
            for doc in docs:
                # take only first document
                content += doc.page_content.replace("\n", "")[:chunk_size]

                # format nicely with source

            output_texts.append(f"###\n{content}")
        except Exception as e:
            logger.info(f"Url: {url} failed to load.")

    # Combine into single text block
    print(output_texts)
    return "\n".join(output_texts)
