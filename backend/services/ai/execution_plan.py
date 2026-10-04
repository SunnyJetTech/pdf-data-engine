from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class ExecutionPlan:

    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    tool_call_id: str | None = None