from enum import Enum

class MessageRole(str, Enum):

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class ChatStatus(str, Enum):

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"