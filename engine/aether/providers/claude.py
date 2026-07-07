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
        
    async def initialize(self):
        # We'll set up the client, even if API key is empty initially.
        # It'll fail on test_connection or chat if invalid.
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.client = AsyncAnthropic(api_key=api_key)
        
        self.models = [
            ModelInfo(
                "claude-3-5-sonnet-20240620", 
                "Claude 3.5 Sonnet", 
                200000, 
                "Most intelligent model, balanced speed and cost",
                ["vision", "tools", "fast"]
            ),
            ModelInfo(
                "claude-3-opus-20240229", 
                "Claude 3 Opus", 
                200000, 
                "Highest performance on complex tasks",
                ["vision", "tools", "reasoning"]
            ),
            ModelInfo(
                "claude-3-haiku-20240307", 
                "Claude 3 Haiku", 
                200000, 
                "Fastest and most compact model",
                ["vision", "fast"]
            )
        ]
        self.status = "connected" if api_key else "disconnected"
        
    async def test_connection(self) -> Tuple[bool, float, str]:
        if not self.client:
            return False, 0.0, "Client not initialized"
            
        start = time.time()
        try:
            # Minimal request to test auth
            await self.client.messages.create(
                max_tokens=10,
                messages=[{"role": "user", "content": "hello"}],
                model="claude-3-haiku-20240307"
            )
            latency = (time.time() - start) * 1000
            self.status = "connected"
            return True, latency, ""
        except Exception as e:
            self.status = "error"
            return False, 0.0, str(e)
            
    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        if not self.client:
            raise ValueError("Anthropic client not configured")
            
        async with self.client.messages.stream(
            max_tokens=4096,
            messages=messages,
            model=model_id
        ) as stream:
            async for text in stream.text_stream:
                yield text
