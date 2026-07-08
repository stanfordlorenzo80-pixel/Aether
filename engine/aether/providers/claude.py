import os
import time
import asyncio
from typing import List, AsyncGenerator, Tuple
from anthropic import AsyncAnthropic
from aether.providers.base import BaseProvider, ModelInfo

class ClaudeProvider(BaseProvider):
    def __init__(self):
        super().__init__("claude", "Anthropic Claude", "cloud")
        self.client = None
        self._api_key = ""
        
    async def initialize(self):
        self._api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if self._api_key:
            self.client = AsyncAnthropic(api_key=self._api_key)
        
        # Always register the model catalog regardless of key status
        self.models = [
            ModelInfo(
                "claude-sonnet-4-20250514", 
                "Claude Sonnet 4", 
                200000, 
                "Latest and most intelligent Sonnet model",
                ["vision", "tools", "fast", "reasoning"]
            ),
            ModelInfo(
                "claude-3-5-sonnet-20241022", 
                "Claude 3.5 Sonnet v2", 
                200000, 
                "Previous generation Sonnet, still excellent",
                ["vision", "tools", "fast"]
            ),
            ModelInfo(
                "claude-3-5-haiku-20241022", 
                "Claude 3.5 Haiku", 
                200000, 
                "Fastest and most compact model",
                ["vision", "fast"]
            ),
            ModelInfo(
                "claude-3-opus-20240229", 
                "Claude 3 Opus", 
                200000, 
                "Highest performance on complex tasks",
                ["vision", "tools", "reasoning"]
            ),
        ]
        self.status = "connected" if self._api_key else "disconnected"

    def set_api_key(self, key: str):
        """Hot-swap API key at runtime."""
        self._api_key = key
        os.environ["ANTHROPIC_API_KEY"] = key
        if key:
            self.client = AsyncAnthropic(api_key=key)
            self.status = "connected"
        else:
            self.client = None
            self.status = "disconnected"
        
    async def test_connection(self) -> Tuple[bool, float, str]:
        if not self.client or not self._api_key:
            return False, 0.0, "API key not configured"
            
        start = time.time()
        try:
            await self.client.messages.create(
                max_tokens=10,
                messages=[{"role": "user", "content": "hello"}],
                model="claude-3-5-haiku-20241022"
            )
            latency = (time.time() - start) * 1000
            self.status = "connected"
            return True, latency, ""
        except Exception as e:
            self.status = "error"
            return False, 0.0, str(e)
            
    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        if not self.client:
            raise ValueError("Anthropic API key not configured. Go to Settings to add your key.")
            
        async with self.client.messages.stream(
            max_tokens=4096,
            messages=messages,
            model=model_id
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def chat(self, model_id: str, messages: List[dict]) -> str:
        if not self.client:
            raise ValueError("Anthropic API key not configured. Go to Settings to add your key.")
            
        response = await self.client.messages.create(
            max_tokens=4096,
            messages=messages,
            model=model_id
        )
        return response.content[0].text

    async def shutdown(self):
        pass
