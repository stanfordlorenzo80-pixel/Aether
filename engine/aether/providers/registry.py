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

    def _get_provider_status(self, name: str) -> str:
        """Map connection tuple to a frontend-friendly status string."""
        status = self._connection_status.get(name)
        if status is None:
            return "disconnected"
        if status[0]:
            return "connected"
        # Has been tested but failed
        provider = self._providers.get(name)
        if provider and provider.status == "error":
            return "error"
        return "disconnected"

    def list_providers(self) -> list[dict[str, Any]]:
        """Return providers with nested models — matches frontend ProviderInfo shape."""
        results: list[dict[str, Any]] = []
        for name, provider in self._providers.items():
            status_tuple = self._connection_status.get(name)
            pstatus = self._get_provider_status(name)

            # Build nested model list (ALWAYS include models regardless of connection)
            models = []
            for m in provider.models:
                models.append({
                    "id": m.id,
                    "name": m.name,
                    "provider": name,
                    "contextWindow": m.context_window,
                    "description": m.description,
                    "capabilities": m.capabilities,
                })

            results.append({
                "id": name,
                "name": provider.name,
                "type": provider.type,
                "status": pstatus,
                "models": models,
                "latency_ms": round(status_tuple[1], 1) if status_tuple else 0.0,
                "error": status_tuple[2] if status_tuple and not status_tuple[0] else "",
            })
        return results

    async def list_all_models(self) -> list[dict[str, Any]]:
        """Flat list of ALL models across ALL providers (regardless of connection)."""
        all_models: list[dict[str, Any]] = []
        for name, provider in self._providers.items():
            for m in provider.models:
                all_models.append({
                    "id": m.id,
                    "name": m.name,
                    "provider": name,
                    "contextWindow": m.context_window,
                    "description": m.description,
                    "capabilities": m.capabilities,
                })
        return all_models

    def update_api_key(self, provider_name: str, api_key: str) -> bool:
        """Hot-swap an API key for a provider."""
        provider = self._providers.get(provider_name)
        if provider is None:
            return False
        if hasattr(provider, "set_api_key"):
            provider.set_api_key(api_key)
            return True
        return False

    def update_ollama_url(self, url: str) -> bool:
        """Hot-swap the Ollama base URL."""
        provider = self._providers.get("ollama")
        if provider is None:
            return False
        if hasattr(provider, "set_base_url"):
            provider.set_base_url(url)
            return True
        return False

    async def refresh_provider(self, name: str) -> dict[str, Any]:
        """Re-initialize and re-test a single provider."""
        provider = self._providers.get(name)
        if provider is None:
            return {"success": False, "error": "Provider not found"}
        
        await provider.initialize()
        status = await provider.test_connection()
        self._connection_status[name] = status
        
        return {
            "success": status[0],
            "latency_ms": round(status[1], 1),
            "error": status[2],
            "models_count": len(provider.models),
        }

    async def initialize(self) -> None:
        logger.info("Initialising provider registry …")

        # ── Claude ───────────────────────────────────────────────────────
        claude = ClaudeProvider()
        await claude.initialize()
        self.register(claude)
        claude_status = await claude.test_connection()
        self._connection_status["claude"] = claude_status
        if claude_status[0]:
            logger.info("✓ Claude connected (%.0fms)", claude_status[1])
        else:
            logger.warning("✗ Claude not connected: %s", claude_status[2])

        # ── Ollama ───────────────────────────────────────────────────────
        ollama = OllamaProvider()
        await ollama.initialize()
        self.register(ollama)
        ollama_status = await ollama.test_connection()
        self._connection_status["ollama"] = ollama_status
        if ollama_status[0]:
            logger.info("✓ Ollama detected (%d model(s), %.0fms)", len(ollama.models), ollama_status[1])
        else:
            logger.debug("Ollama not detected — skipping local provider")
            
        # ── OpenRouter ───────────────────────────────────────────────────
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
        total_models = sum(len(p.models) for p in self._providers.values())
        logger.info(
            "Registry ready — %d provider(s) connected, %d total models: %s",
            len(connected), total_models, ", ".join(connected) or "none"
        )

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
