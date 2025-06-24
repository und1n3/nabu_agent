from workflows.main.workflow import execute_main_workflow


def main():
    print("Hola sóc en nabu-agent! En què puc ajudar-te?")
    execute_main_workflow("Hola posa una cançó")


if __name__ == "__main__":
    main()
