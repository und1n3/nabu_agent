import logging

from dotenv import load_dotenv

from .workflows.main.workflow import execute_main_workflow

load_dotenv()

logger = logging.getLogger(__name__)

logging.basicConfig(filename="nabu_agent_agent.log", level=logging.INFO, filemode="w+")


def main():
    res = execute_main_workflow("hola")
    logger.info(res)
    print("f")


if __name__ == "__main__":
    main()
