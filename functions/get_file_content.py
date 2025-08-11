import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    #target_dir = abs_working_dir

    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        MAX_CHARS = 10000
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        return file_content_string
    except Exception as e:
        return f"Error: Cannot read file: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_content",
    description="Reads the contents of a given file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read content from, relative to the working directory.",
            ),
        },
    ),
)