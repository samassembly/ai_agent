import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)

    #set filepath
    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ['python', target_file] + args,
            cwd=abs_working_dir,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        exit_code = completed_process.returncode

        output_parts = [
            f"STDOUT:\n{stdout if stdout else '[No output]'}",
            f"STDERR:\n{stderr if stderr else '[No errors]'}"
        ]

        if exit_code != 0:
            output_parts.append(f"Process exited with code {exit_code}")

        return "\n\n".join(output_parts)


    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python program at the given file path within the working directory, using any provided arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python program to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of arguments to provide to the python program to run",
            ),
        },
    ),
)