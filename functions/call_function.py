import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    #Call the function
    working_directory = "./calculator"
    function_name = function_call_part.name
    if function_name == "get_file_content":
        function_result = get_file_content(working_directory, **(function_call_part.args))
    if function_name == "get_files_info":
        function_result = get_files_info(working_directory, **(function_call_part.args))
    if function_name == "run_python":
        function_result = run_python_file(working_directory, **(function_call_part.args))
    if function_name == "write_file":
        function_result = write_file(working_directory, **(function_call_part.args))
    else:
        #If the function is invalid
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    #Otherwise
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )