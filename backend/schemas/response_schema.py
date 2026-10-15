from __future__ import annotations
from typing import Any
from pydantic import BaseModel, ConfigDict

class APIResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    success: bool = True
    message: str | None = None
    data: Any = None