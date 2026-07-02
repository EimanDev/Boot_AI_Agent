import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    user_input = args.user_prompt
    is_verbose = args.verbose

    # OpenAI SDK uses plain dicts for messages, not types.Content
    messages = [
        {"role": "user", "content": user_input}
    ]

    # The method is chat.completions.create, and the key is "messages" not "contents"
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if is_verbose:
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    # Access the response text via choices, not .text
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
