# main.py

import os
from dotenv import load_dotenv

from chat_session import ChatSession

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
    chat_session = ChatSession(config)
    chat_session.run()

if __name__ == "__main__":
    main()

