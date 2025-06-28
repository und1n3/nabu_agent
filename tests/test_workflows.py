from workflows.main.workflow import execute_main_workflow


def test_full_run_1():
    input_prompt = "Posa una cancó de Mika"
    result = execute_main_workflow(user_input=input_prompt)
    assert result == ""
