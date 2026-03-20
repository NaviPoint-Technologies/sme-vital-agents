# @section Tool Registry
"""Registry for discovering and resolving tools by name."""

from __future__ import annotations

from typing import Type

from core.tools.base import Tool


# @subsection ToolRegistry
class ToolRegistry:
    """Maps tool names to their implementations."""

    _tools: dict[str, Type[Tool]] = {}

    @classmethod
    def register(cls, tool_cls: Type[Tool]) -> Type[Tool]:
        """Register a tool class. Can be used as a decorator."""
        cls._tools[tool_cls.name] = tool_cls
        return tool_cls

    @classmethod
    def resolve(cls, names: list[str]) -> list[Tool]:
        """Instantiate tools by name."""
        resolved = []
        for name in names:
            tool_cls = cls._tools.get(name)
            if tool_cls:
                resolved.append(tool_cls())
        return resolved

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._tools.keys())
