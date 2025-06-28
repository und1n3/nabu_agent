from workflows.main.workflow import execute_main_workflow
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="nabu_langgraph_agent.log", level=logging.INFO)


def main():
    print("Hola sóc en nabu-agent! En què puc ajudar-te?")
    execute_main_workflow("Hola posa una cançó")


if __name__ == "__main__":
    main()
