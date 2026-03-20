# @section Tool Base
"""Abstract tool interface for agent capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


# @subsection Tool ABC
class Tool(ABC):
    """A capability that an agent can invoke."""

    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Run the tool with the given arguments."""
        ...

    def schema(self) -> dict:
        """Return an OpenAI-compatible tool/function schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters(),
            },
        }

    def parameters(self) -> dict:
        """Override to define JSON Schema parameters."""
        return {"type": "object", "properties": {}}
