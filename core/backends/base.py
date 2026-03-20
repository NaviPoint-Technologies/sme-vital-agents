# @section Backend Base
"""Abstract backend interface for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


# @subsection BackendConfig
class BackendConfig(BaseModel):
    """Configuration for a backend provider."""

    name: str
    model: str
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    extra: dict[str, Any] = {}


# @subsection Backend ABC
class Backend(ABC):
    """Abstract base class for all LLM backends."""

    def __init__(self, config: BackendConfig) -> None:
        self.config = config

    @abstractmethod
    async def generate(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Generate a response from the backend.

        Args:
            messages: Chat messages in OpenAI-compatible format.
            tools: Optional tool definitions for function calling.

        Returns:
            Response dict with 'content' and optional 'tool_calls'.
        """
        ...

    @abstractmethod
    async def stream(self, messages: list[dict], tools: list[dict] | None = None):
        """Stream a response from the backend. Yields chunks."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the backend is reachable and operational."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.config.model!r})"
