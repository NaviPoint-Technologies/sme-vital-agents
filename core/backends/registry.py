# @section Backend Registry
"""Registry for discovering and instantiating backends."""

from __future__ import annotations

from typing import Type

from core.backends.base import Backend, BackendConfig


# @subsection BackendRegistry
class BackendRegistry:
    """Central registry mapping backend names to their implementations."""

    _backends: dict[str, Type[Backend]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a backend class."""

        def decorator(backend_cls: Type[Backend]):
            cls._backends[name] = backend_cls
            return backend_cls

        return decorator

    @classmethod
    def create(cls, config: BackendConfig) -> Backend:
        """Instantiate a backend from config."""
        backend_cls = cls._backends.get(config.name)
        if not backend_cls:
            available = ", ".join(cls._backends.keys()) or "(none)"
            raise ValueError(
                f"Unknown backend '{config.name}'. Available: {available}"
            )
        return backend_cls(config)

    @classmethod
    def available(cls) -> list[str]:
        """List registered backend names."""
        return list(cls._backends.keys())
