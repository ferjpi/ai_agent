import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    try:
        common_path = os.path.commonpath([abs_working_directory, abs_file_path])
        if common_path != abs_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(abs_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file where the content will be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The content to write to the file."
            ),
        },
    ),
)
