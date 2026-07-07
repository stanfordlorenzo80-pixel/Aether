"""Provider registry — singleton that owns and orchestrates all LLM providers."""

from __future__ import annotations

import logging
from typing import Any

from aether.config import config
from aether.providers.base import (
    ConnectionStatus,
    ModelInfo,
    ModelProvider,
)
from aether.providers.claude import ClaudeProvider
from aether.providers.ollama import OllamaProvider

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """Central registry for all configured LLM providers.

    Typical lifecycle::

        registry = ProviderRegistry()
        await registry.initialize()   # probes providers, caches model lists
        ...
        await registry.shutdown()     # tears down HTTP clients
    """

    _instance: ProviderRegistry | None = None

    def __new__(cls) -> ProviderRegistry:
        """Ensure singleton — only one registry per process."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._providers = {}
            cls._instance._connection_status = {}
        return cls._instance

    # ── Registration ────────────────────────────────────────────────────

    def register(self, provider: ModelProvider) -> None:
        """Add a provider to the registry."""
        self._providers[provider.name] = provider
        logger.info("Registered provider: %s (%s)", provider.name, provider.provider_type.value)

    def unregister(self, name: str) -> None:
        """Remove a provider by name."""
        self._providers.pop(name, None)
        self._connection_status.pop(name, None)

    # ── Lookup ──────────────────────────────────────────────────────────

    def get_provider(self, name: str) -> ModelProvider | None:
        """Retrieve a provider by name, or ``None`` if not registered."""
        return self._providers.get(name)

    def get_default_provider(self) -> ModelProvider | None:
        """Return the provider named in ``config.default_provider``."""
        return self._providers.get(config.default_provider)

    def resolve_provider_for_model(self, model_id: str) -> ModelProvider | None:
        """Find the provider that owns *model_id*.

        Checks cached model lists, falling back to the default provider.
        """
        # Quick heuristic: claude-* → claude, everything else → check caches.
        if model_id.startswith("claude"):
            provider = self._providers.get("claude")
            if provider is not None:
                return provider

        # Walk every provider's cached models.
        for provider in self._providers.values():
            if hasattr(provider, "_cached_models"):
                for m in provider._cached_models:  # noqa: SLF001
                    if m.id == model_id:
                        return provider

        return self.get_default_provider()

    # ── Aggregate queries ───────────────────────────────────────────────

    def list_providers(self) -> list[dict[str, Any]]:
        """Return summary dicts for every registered provider."""
        results: list[dict[str, Any]] = []
        for name, provider in self._providers.items():
            status = self._connection_status.get(name)

            # Ollama has a special 'detected' flag.
            if isinstance(provider, OllamaProvider):
                availability = "available" if provider.detected else "not_detected"
            elif status is not None:
                availability = "available" if status.connected else "unavailable"
            else:
                availability = "unknown"

            results.append(
                {
                    "name": name,
                    "type": provider.provider_type.value,
                    "status": availability,
                    "latency_ms": round(status.latency_ms, 1) if status else 0,
                    "error": status.error if status and not status.connected else "",
                }
            )
        return results

    async def list_all_models(self) -> list[ModelInfo]:
        """Aggregate models from every connected provider."""
        all_models: list[ModelInfo] = []
        for provider in self._providers.values():
            # Only include models from providers that are actually reachable.
            if isinstance(provider, OllamaProvider) and not provider.detected:
                continue
            status = self._connection_status.get(provider.name)
            if status is not None and not status.connected and not isinstance(provider, OllamaProvider):
                continue
            try:
                models = await provider.list_models()
                all_models.extend(models)
            except Exception:  # noqa: BLE001
                logger.debug("Failed to list models for provider %s", provider.name)
        return all_models

    # ── Lifecycle ───────────────────────────────────────────────────────

    async def initialize(self) -> None:
        """Create, register, and probe all configured providers."""
        logger.info("Initialising provider registry …")

        # ── Claude (primary) ────────────────────────────────────────────
        claude = ClaudeProvider(api_key=config.anthropic_api_key)
        self.register(claude)
        claude_status = await claude.test_connection()
        self._connection_status["claude"] = claude_status
        if claude_status.connected:
            logger.info("✓ Claude connected (%.0fms)", claude_status.latency_ms)
        else:
            logger.warning("✗ Claude not connected: %s", claude_status.error)

        # ── Ollama (auto-detect, silent on failure) ─────────────────────
        ollama = OllamaProvider(base_url=config.ollama_base_url)
        self.register(ollama)
        ollama_status = await ollama.test_connection()
        self._connection_status["ollama"] = ollama_status
        if ollama_status.connected:
            models = await ollama.list_models()
            logger.info(
                "✓ Ollama detected (%d model(s), %.0fms)",
                len(models),
                ollama_status.latency_ms,
            )
        else:
            # Debug-level only — missing Ollama is perfectly normal.
            logger.debug("Ollama not detected — skipping local provider")

        connected = [n for n, s in self._connection_status.items() if s.connected]
        logger.info("Registry ready — %d provider(s) connected: %s", len(connected), ", ".join(connected) or "none")

    async def shutdown(self) -> None:
        """Shut down all registered providers and reset singleton state."""
        logger.info("Shutting down provider registry …")
        for name, provider in self._providers.items():
            try:
                await provider.shutdown()
                logger.debug("Provider %s shut down", name)
            except Exception:  # noqa: BLE001
                logger.exception("Error shutting down provider %s", name)

        self._providers.clear()
        self._connection_status.clear()
        ProviderRegistry._instance = None
        logger.info("Provider registry shut down")
