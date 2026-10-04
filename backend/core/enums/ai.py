from enum import Enum

class AIProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    LLAMA = "llama"

class AIModel(str, Enum):
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"