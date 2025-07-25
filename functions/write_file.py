import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    if not file_path:
        return 'Error: No file path provided'

    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Check if a directory exists at the file path
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" because it is a directory'

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: Cannot write to file: {e}"
