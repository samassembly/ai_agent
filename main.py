import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    #Check for prompt argument
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    system_prompt = """
                    You are a helpful AI coding agent.

                    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files

                    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    model_name = 'gemini-2.0-flash-001'
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
    )

    #Calling generate content model loop
    
    for i in range(20):
        try: 
            response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
        except google.genai.errors.ClientError as e:
            print(f"An error has occurred: {e}")

        if response.text:
            print(response.text)
            break #response found, break out of loop
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        function_call_part = response.function_calls[0]
        response_candidates = response.candidates
        #Loop candidates and append to messages list
        for candidate in response_candidates:
            messages.append(candidate.content)
        #convert function_responses into a message with role of user

    
    #Check for verbose
    if '--verbose' in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    if function_call_part:
        function_call_result = call_function(function_call_part)
        print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
