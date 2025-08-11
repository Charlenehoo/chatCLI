# messages.py

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Message:
    role: Role
    content: str

@dataclass
class SystemMessage(Message):
    name: Optional[str] = None

@dataclass
class UserMessage(Message):
    name: Optional[str] = None

@dataclass
class AssistantMessage(Message):
    name: Optional[str]
    prefix: bool = False
    reasoning_content: Optional[str] = None

class Messages(list):

    def append(self, message: dict):
        return super().append(message)
    
    def dump(self):
        pass

    def load(self):
        pass

