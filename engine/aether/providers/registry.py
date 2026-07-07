"""Provider registry — singleton that owns and orchestrates all LLM providers."""

from __future__ import annotations

import logging
from typing import Any

from aether.config import config
from aether.providers.base import (
    ModelInfo,
    BaseProvider,
)
from aether.providers.claude import ClaudeProvider
from aether.providers.ollama import OllamaProvider
from aether.providers.openrouter import OpenRouterProvider

logger = logging.getLogger(__name__)


class ProviderRegistry:
    _instance: ProviderRegistry | None = None

    def __new__(cls) -> ProviderRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._providers = {}
            cls._instance._connection_status = {}
        return cls._instance

    def register(self, provider: BaseProvider) -> None:
        self._providers[provider.name] = provider
        logger.info("Registered provider: %s (%s)", provider.name, provider.type)

    def unregister(self, name: str) -> None:
        self._providers.pop(name, None)
        self._connection_status.pop(name, None)

    def get_provider(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    def get_default_provider(self) -> BaseProvider | None:
        return self._providers.get(config.default_provider)

    def resolve_provider_for_model(self, model_id: str) -> BaseProvider | None:
        if model_id.startswith("claude"):
            provider = self._providers.get("claude")
            if provider is not None:
                return provider

        for provider in self._providers.values():
            if hasattr(provider, "models"):
                for m in provider.models:
                    if m.id == model_id:
                        return provider

        return self.get_default_provider()

    def list_providers(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for name, provider in self._providers.items():
            status = self._connection_status.get(name)
            
            # Using tuple (success, latency, error) logic correctly
            if status is not None:
                availability = "available" if status[0] else "unavailable"
            else:
                availability = "unknown"

            results.append(
                {
                    "name": name,
                    "type": provider.type,
                    "status": availability,
                    "latency_ms": round(status[1], 1) if status else 0.0,
                    "error": status[2] if status and not status[0] else "",
                }
            )
        return results

    async def list_all_models(self) -> list[ModelInfo]:
        all_models: list[ModelInfo] = []
        for provider in self._providers.values():
            status = self._connection_status.get(provider.name)
            if status is not None and not status[0]:
                continue
            try:
                # Most models are fetched during initialize() into self.models
                if hasattr(provider, "models"):
                    all_models.extend(provider.models)
            except Exception:  # noqa: BLE001
                logger.debug("Failed to list models for provider %s", provider.name)
        return all_models

    async def initialize(self) -> None:
        logger.info("Initialising provider registry …")

        claude = ClaudeProvider()
        await claude.initialize()
        self.register(claude)
        claude_status = await claude.test_connection()
        self._connection_status["claude"] = claude_status
        if claude_status[0]:
            logger.info("✓ Claude connected (%.0fms)", claude_status[1])
        else:
            logger.warning("✗ Claude not connected: %s", claude_status[2])

        ollama = OllamaProvider()
        await ollama.initialize()
        self.register(ollama)
        ollama_status = await ollama.test_connection()
        self._connection_status["ollama"] = ollama_status
        if ollama_status[0]:
            logger.info("✓ Ollama detected (%d model(s), %.0fms)", len(ollama.models), ollama_status[1])
        else:
            logger.debug("Ollama not detected — skipping local provider")
            
        openrouter = OpenRouterProvider()
        await openrouter.initialize()
        self.register(openrouter)
        openrouter_status = await openrouter.test_connection()
        self._connection_status["openrouter"] = openrouter_status
        if openrouter_status[0]:
            logger.info("✓ OpenRouter connected (%.0fms)", openrouter_status[1])
        else:
            logger.warning("✗ OpenRouter not connected: %s", openrouter_status[2])

        connected = [n for n, s in self._connection_status.items() if s[0]]
        logger.info("Registry ready — %d provider(s) connected: %s", len(connected), ", ".join(connected) or "none")

    async def shutdown(self) -> None:
        logger.info("Shutting down provider registry …")
        for name, provider in self._providers.items():
            if hasattr(provider, "shutdown"):
                try:
                    await provider.shutdown()
                    logger.debug("Provider %s shut down", name)
                except Exception:
                    logger.exception("Error shutting down provider %s", name)

        self._providers.clear()
        self._connection_status.clear()
        ProviderRegistry._instance = None
        logger.info("Provider registry shut down")
