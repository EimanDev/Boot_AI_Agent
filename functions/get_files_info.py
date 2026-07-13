import os

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
        if directory == ".":
            string_list = ["Result for current directory:"]
        else:
            string_list = [f"Result for {directory} directory:"]
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            dir_list = os.listdir(target_dir)

            for item in dir_list:
                full_path = os.path.join(target_dir, item)
                item_string = f"- {item}: file_size={os.path.getsize(full_path)} bytes, is_dir={
                    os.path.isdir(full_path)}"
                string_list.append(item_string)
        return "\n".join(string_list)
    except Exception as e:
        return f"Error: {e}"
