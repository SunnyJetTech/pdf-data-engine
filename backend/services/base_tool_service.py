from __future__ import annotations
from context.tool_context import ToolContext

class BaseToolService:
    def __init__(self, context: ToolContext):
        self.context = context
        self.db = context.db
        self.user = context.user
        self.dataset = context.dataset
        self.session = context.session
        self.memory = context.memory
        self.dataframe = context.dataframe
        self.runtime = context.runtime or {}

    @property
    def collection_name(self) -> str:
        return self.dataset.storage_identifier

    def set_dataframe(self, dataframe):
        self.context.dataframe = dataframe
        self.dataframe = dataframe

    def get_dataframe(self):
        return self.dataframe