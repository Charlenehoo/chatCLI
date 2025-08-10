# main.py

import os
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from openai import OpenAI

def get_config():
    load_dotenv()
    config = {
        "api_key": os.getenv("API_KEY"),
        "base_url": os.getenv("BASE_URL"),
        "model": os.getenv("MODEL"),
    }
    return config

def main():
    config = get_config()
    prompt_session = PromptSession()
    client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
    print(f"model: {config['model']}")
    while True:
        user_input = prompt_session.prompt(message="> ")
        if not user_input.strip():
            continue
        if user_input.lower() == "quit":
            break
        response = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"{user_input}"},
            ],
            stream=False
        )
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()

