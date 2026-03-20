# @section Ollama Backend
"""Backend for local LLMs via Ollama."""

from __future__ import annotations

import httpx

from core.backends.base import Backend, BackendConfig
from core.backends.registry import BackendRegistry


# @subsection OllamaBackend
@BackendRegistry.register("ollama")
class OllamaBackend(Backend):
    """Run agents against local Ollama models."""

    def __init__(self, config: BackendConfig) -> None:
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"

    async def generate(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        payload: dict = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()

        message = data.get("message", {})
        return {
            "content": message.get("content", ""),
            "tool_calls": message.get("tool_calls"),
        }

    async def stream(self, messages: list[dict], tools: list[dict] | None = None):
        payload: dict = {
            "model": self.config.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
        }
        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                import json as _json

                async for line in resp.aiter_lines():
                    if line.strip():
                        chunk = _json.loads(line)
                        msg = chunk.get("message", {})
                        if content := msg.get("content"):
                            yield content

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except httpx.HTTPError:
            return False
