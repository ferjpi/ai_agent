import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    prompt = ""
    flag = False

    
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        cmd_flag = sys.argv[2:]
        if "--verbose" in cmd_flag:
            flag = True
    else:
        print("Usage: python main.py [prompt]")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(response.text)
    if flag:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
