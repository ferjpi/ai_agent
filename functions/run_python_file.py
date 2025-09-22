import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    try:
        common_path = os.path.commonpath([abs_working_directory, abs_file_path])
        if common_path != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python3", abs_file_path] + args,
                cwd=abs_working_directory,
                capture_output=True,
                timeout=30,
                text=True,
            )

            if result.returncode == 0:
                if len(result.stdout) == 0:
                    return f"STDOUT: No output produced."
                return f"STDOUT: " + result.stdout
            else:
                return (
                    f"STDERR: "
                    + result.stderr
                    + f"\nProcess existed with code {result.returncode}"
                )

        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute. Must be a Python file.",
            )
        },
    ),
)
