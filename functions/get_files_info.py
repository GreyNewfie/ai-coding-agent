import os.path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        directory_abs = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, directory_abs]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory_abs):
            return f'Error: "{directory}" is not a directory'

        directory_items = os.listdir(directory_abs)
        contents: list[str] = []

        for filename in directory_items:
            filepath = os.path.join(directory_abs, filename)
            name = filename
            file_size = os.path.getsize(filepath)
            is_directory = os.path.isdir(filepath)
            contents.append(f"   - {name}: file_size={file_size}, is_dir={is_directory}")

        return "\n".join(contents)

    except Exception as e:
        return f'Error: {e}'
