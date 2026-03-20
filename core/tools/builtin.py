# @section Built-in Tools
"""Bundled tools available to all agents."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from core.tools.base import Tool
from core.tools.registry import ToolRegistry


# @subsection ReadFileTool
@ToolRegistry.register
class ReadFileTool(Tool):
    name = "read_file"
    description = "Read the contents of a file at the given path."

    async def execute(self, path: str = "", **kwargs: Any) -> str:
        try:
            return Path(path).read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading {path}: {e}"

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File path to read"}},
            "required": ["path"],
        }


# @subsection WriteFileTool
@ToolRegistry.register
class WriteFileTool(Tool):
    name = "write_file"
    description = "Write content to a file, creating directories as needed."

    async def execute(self, path: str = "", content: str = "", **kwargs: Any) -> str:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Wrote {len(content)} chars to {path}"
        except Exception as e:
            return f"Error writing {path}: {e}"

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to write"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        }


# @subsection ShellTool
@ToolRegistry.register
class ShellTool(Tool):
    name = "shell"
    description = "Execute a shell command and return stdout/stderr."

    async def execute(self, command: str = "", **kwargs: Any) -> str:
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=60
            )
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR: {result.stderr}"
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            return "Error: command timed out (60s)"
        except Exception as e:
            return f"Error: {e}"

    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "Shell command to run"}},
            "required": ["command"],
        }
