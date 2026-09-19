import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        output = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_dir]
            if args is not None:
                command.extend(args)
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)
            if result.returncode != 0:
                output += f"Process exited with code {result.returncode}"
            if not result.stdout and not result.stderr:
                output += "No output produced"
            if result.stdout:
                output += f"STDOUT:{result.stdout}"
            if result.stderr:
                output += f"STDERR:{result.stderr}"
        return output

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file with provided args",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional arguments to pass to the python file, as a list of strings"
                },
            },
        },
    },
}
