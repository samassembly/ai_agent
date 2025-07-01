import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    #Check for verbose
    if '--verbose' in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(response.text)

if __name__ == "__main__":
    main()
