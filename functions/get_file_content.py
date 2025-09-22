import os
from config import max_number_of_characters
from google.genai import types


def get_file_content(working_directory, file_path):
    original_path = file_path
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        common_path = os.path.commonpath([working_directory, file_path])
        if common_path != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_path):
        return f'Error: File not found or is not a regular file: "{original_path}"'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{original_path}"'

    if not os.access(file_path, os.R_OK):
        return f'Error: Cannot read "{file_path}" as it is not readable'

    try:
        with open(file_path, "r") as f:
            content = f.read(max_number_of_characters)

            if os.path.getsize(file_path) > max_number_of_characters:
                content = (
                    content
                    + f'[...File "{original_path}" truncated at {max_number_of_characters} characters]'
                )

            return content
    except Exception as e:
        return f'Error reading file "{original_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file where the content will be extracted.",
            )
        },
    ),
)
