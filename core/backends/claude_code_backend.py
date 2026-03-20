# @section Claude Code Backend
"""Backend that shells out to Claude Code CLI — no API keys needed."""

from __future__ import annotations

import asyncio
import json

from core.backends.base import Backend, BackendConfig
from core.backends.registry import BackendRegistry


# @subsection ClaudeCodeBackend
@BackendRegistry.register("claude-code")
class ClaudeCodeBackend(Backend):
    """Run agents via the Claude Code CLI (claude command).

    Requires `claude` CLI installed and authenticated.
    No API key or direct API usage — everything goes through the CLI.
    """

    def __init__(self, config: BackendConfig) -> None:
        super().__init__(config)
        self.cli_command = config.extra.get("cli_command", "claude")

    async def generate(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        prompt = self._messages_to_prompt(messages)

        proc = await asyncio.create_subprocess_exec(
            self.cli_command,
            "--print",
            "--output-format", "json",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate(input=prompt.encode())

        if proc.returncode != 0:
            raise RuntimeError(f"Claude Code CLI error: {stderr.decode()}")

        try:
            data = json.loads(stdout.decode())
            content = data.get("result", stdout.decode())
        except json.JSONDecodeError:
            content = stdout.decode()

        return {"content": content, "tool_calls": None}

    async def stream(self, messages: list[dict], tools: list[dict] | None = None):
        prompt = self._messages_to_prompt(messages)

        proc = await asyncio.create_subprocess_exec(
            self.cli_command,
            "--print",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        assert proc.stdout is not None
        assert proc.stdin is not None
        proc.stdin.write(prompt.encode())
        proc.stdin.close()

        async for line in proc.stdout:
            yield line.decode()

        await proc.wait()

    async def health_check(self) -> bool:
        try:
            proc = await asyncio.create_subprocess_exec(
                self.cli_command,
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.communicate()
            return proc.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    def _messages_to_prompt(messages: list[dict]) -> str:
        """Flatten chat messages into a single prompt string for the CLI."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append(f"[System]\n{content}")
            elif role == "assistant":
                parts.append(f"[Assistant]\n{content}")
            else:
                parts.append(content)
        return "\n\n".join(parts)
