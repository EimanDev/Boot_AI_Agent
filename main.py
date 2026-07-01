import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    # Declare a parser
    parser = argparse.ArgumentParser(description="Chatbot")

    # Add arguments to the parser
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    # Safe parse args
    args = parser.parse_args()

    # Now we can access all arg arguments
    user_input = args.user_prompt
    is_verbose = args.verbose
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    prompt = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )
    prompt_metadata = prompt.usage_metadata

    if prompt_metadata is not None and is_verbose is True:
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {prompt_metadata.prompt_token_count}")
        print(f"Response tokens: {prompt_metadata.candidates_token_count}")
    elif prompt_metadata is None:
        raise RuntimeError("API request failed")

    print(prompt.text)


if __name__ == "__main__":
    main()
