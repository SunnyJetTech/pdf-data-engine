from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ChatStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"