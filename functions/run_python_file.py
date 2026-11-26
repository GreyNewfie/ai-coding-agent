import os.path
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python file at a specified file path relative to the working directory and return its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the python file to run"
                },
                "args": {
                    "type": "array",
                    "description": "Additional command line arguments that will be passed to the python file being executed",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))

        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args and len(args) > 0:
           command.extend(args)

        result = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30, check=False)
        output: str = ""

        if result.returncode != 0:
           output += f'Process exited with code {result.returncode}'

        if not result.stderr and not result.stdout:
            output += 'No output produced'
        else:
            output += f'STDOUT: {result.stdout} STDERR: {result.stderr}'

        return output
    except Exception as e:
        return f'Error: Executing python file: {e}'
