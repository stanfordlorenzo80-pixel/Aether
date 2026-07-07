import json
import os
import time
from typing import List, AsyncGenerator, Tuple
import aiohttp

from aether.providers.base import BaseProvider, ModelInfo

class OpenRouterProvider(BaseProvider):
    def __init__(self):
        super().__init__("openrouter", "OpenRouter", "cloud")
        self.api_key = ""
        self.base_url = "https://openrouter.ai/api/v1"
        self._session = None

    async def initialize(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY", "")
        self.status = "connected" if self.api_key else "disconnected"
        
        if self.api_key:
            try:
                session = await self._get_session()
                async with session.get(f"{self.base_url}/models", timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        models = []
                        for m in data.get("data", []):
                            models.append(ModelInfo(
                                id=m["id"],
                                name=m.get("name", m["id"]),
                                context_window=m.get("context_length", 8192),
                                description="OpenRouter Model"
                            ))
                        self.models = models
            except Exception:
                pass

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

    async def test_connection(self) -> Tuple[bool, float, str]:
        if not self.api_key:
            return False, 0.0, "API key not configured"
        
        start = time.time()
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/models", timeout=5) as resp:
                latency = (time.time() - start) * 1000
                if resp.status == 200:
                    self.status = "connected"
                    return True, latency, ""
                else:
                    self.status = "error"
                    return False, latency, f"HTTP {resp.status}"
        except Exception as e:
            self.status = "error"
            return False, 0.0, str(e)

    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
            
        session = await self._get_session()
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": True,
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

    async def chat(self, model_id: str, messages: List[dict]) -> str:
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
            
        session = await self._get_session()
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": False,
        }
        
        async with session.post(f"{self.base_url}/chat/completions", json=payload) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

    async def shutdown(self):
        if self._session and not self._session.closed:
            await self._session.close()
