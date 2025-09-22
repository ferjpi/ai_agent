import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function
from config import MAX_ITERATIONS


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_write_file,
        schema_get_files_info,
        schema_run_python_file,
    ]
)


def main():
    prompt = ""
    verbose = False

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        cmd_flag = sys.argv[2:]
        if "--verbose" in cmd_flag:
            verbose = True
    else:
        print("Usage: python main.py [prompt]")
        sys.exit(1)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    iter = 0
    while True:
        iter += 1

        if iter > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)

        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Function call failed")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    main()
