# @section Backends Package
"""Pluggable LLM backends — no Claude API, ever."""

from core.backends.base import Backend, BackendConfig
from core.backends.registry import BackendRegistry

__all__ = ["Backend", "BackendConfig", "BackendRegistry"]
