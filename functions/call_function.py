from google.genai import types
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file

list_of_functions = [get_file_content, write_file, get_files_info, run_python_file]


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(" - Calling function:", function_call_part.name)

    function_name = function_call_part.name
    if find_function_by_name(list_of_functions, function_call_part.name) is not None:
        function_result = find_function_by_name(
            list_of_functions, function_call_part.name
        )(working_directory="./calculator", **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


def find_function_by_name(functions, name):
    for function in functions:
        if function.__name__ == name:
            return function
    return None
