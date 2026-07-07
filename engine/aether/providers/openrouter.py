import json
import os
from typing import AsyncGenerator
import aiohttp

from aether.config import config
from aether.providers.base import (
    ConnectionStatus,
    ModelInfo,
    ModelProvider,
    ProviderType,
)

class OpenRouterProvider(ModelProvider):
    name = "openrouter"
    provider_type = ProviderType.CLOUD

    def __init__(self, api_key: str = ""):
        self.api_key = api_key or getattr(config, "openrouter_api_key", os.environ.get("OPENROUTER_API_KEY", ""))
        self.base_url = "https://openrouter.ai/api/v1"
        self._session: aiohttp.ClientSession | None = None
        self._cached_models: list[ModelInfo] = []

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://github.com/stanfordlorenzo80-pixel/Aether",
                    "X-Title": "Aether Engine",
                }
            )
        return self._session

    async def test_connection(self) -> ConnectionStatus:
        if not self.api_key:
            return ConnectionStatus(connected=False, latency_ms=0, error="API key not configured")
        
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/models", timeout=5) as resp:
                if resp.status == 200:
                    return ConnectionStatus(connected=True, latency_ms=0)
                else:
                    return ConnectionStatus(connected=False, latency_ms=0, error=f"HTTP {resp.status}")
        except Exception as e:
            return ConnectionStatus(connected=False, latency_ms=0, error=str(e))

    async def list_models(self) -> list[ModelInfo]:
        if not self.api_key:
            return []
        
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/models") as resp:
                data = await resp.json()
                models = []
                for m in data.get("data", []):
                    models.append(ModelInfo(
                        id=m["id"],
                        name=m.get("name", m["id"]),
                        provider="openrouter",
                        context_window=m.get("context_length", 8192)
                    ))
                self._cached_models = models
                return models
        except Exception:
            return []

    async def stream_chat(
        self, model_id: str, messages: list[dict[str, str]], **kwargs
    ) -> AsyncGenerator[str, None]:
        session = await self._get_session()
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": True,
            **kwargs
        }
        
        async with session.post(f"{self.base_url}/chat/completions", json=payload) as resp:
            async for line in resp.content:
                if line:
                    decoded = line.decode('utf-8').strip()
                    if decoded.startswith("data: ") and decoded != "data: [DONE]":
                        try:
                            chunk = json.loads(decoded[6:])
                            content = chunk["choices"][0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass

    async def shutdown(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
