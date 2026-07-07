import asyncio
import time
from typing import Dict, List, Tuple, AsyncGenerator
from aether.providers.base import BaseProvider
from aether.providers.claude import ClaudeProvider
from aether.providers.ollama import OllamaProvider

class ModelRegistry:
    def __init__(self):
        self.providers: Dict[str, BaseProvider] = {}
        
    async def initialize(self):
        # 1. Initialize Claude (Primary)
        claude = ClaudeProvider()
        await claude.initialize()
        self.providers[claude.id] = claude
        
        # 2. Auto-detect Ollama gracefully
        ollama = OllamaProvider()
        try:
            # We don't block the engine if Ollama is down
            success, _, _ = await ollama.test_connection()
            if success:
                await ollama.initialize()
                self.providers[ollama.id] = ollama
        except Exception:
            # Silent fallback, user doesn't use local
            pass
            
    def get_all_providers_info(self) -> List[dict]:
        # Sort so Claude is always first
        sorted_providers = sorted(
            self.providers.values(), 
            key=lambda p: 0 if p.id == "claude" else 1
        )
        return [p.get_info() for p in sorted_providers]
        
    async def test_connection(self, provider_id: str) -> Tuple[bool, float, str]:
        if provider_id not in self.providers:
            return False, 0.0, f"Provider {provider_id} not found"
        return await self.providers[provider_id].test_connection()
        
    async def stream_chat(self, provider_id: str, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        if provider_id not in self.providers:
            raise ValueError(f"Provider {provider_id} not found")
        
        async for chunk in self.providers[provider_id].stream_chat(model_id, messages):
            yield chunk

    async def chat(self, provider_id: str, model_id: str, messages: List[dict]) -> str:
        if provider_id not in self.providers:
            raise ValueError(f"Provider {provider_id} not found")
        return await self.providers[provider_id].chat(model_id, messages)
