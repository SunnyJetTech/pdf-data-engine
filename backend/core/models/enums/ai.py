from enum import Enum

class ProviderType(str, Enum):

    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    LLAMA = "llama"

class ToolType(str, Enum):

    SEARCH = "search"
    EXPORT = "export"
    SUMMARY = "summary"
    DUPLICATE = "duplicate"
    STATISTICS = "statistics"
    FILTER = "filter"
    MERGE = "merge"