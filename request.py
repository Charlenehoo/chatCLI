# request.py

from dataclasses import dataclass
from messages import Messages

@dataclass
class Request:
    messages: Messages
    model: str
    frequency_penalty: float = 0 # -2 <= frequency_penalty <= 2
    max_tokens: int = 4096 # 1 < max_tokens <= 8192
    presence_penalty: float = 0 # -2 <= presence_penalty <= 2
    stream: bool = False

