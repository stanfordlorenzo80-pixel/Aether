import time
import httpx
import json
from typing import List, AsyncGenerator, Tuple
from aether.providers.base import BaseProvider, ModelInfo

class OllamaProvider(BaseProvider):
    def __init__(self):
        super().__init__("ollama", "Ollama (Local)", "local")
        self.base_url = "http://127.0.0.1:11434"
        self.client = httpx.AsyncClient(timeout=5.0)
        
    async def initialize(self):
        try:
            # Check 127.0.0.1 first
            resp = await self.client.get(f"{self.base_url}/api/tags", timeout=2.0)
            if resp.status_code != 200:
                # Fallback to localhost
                self.base_url = "http://localhost:11434"
                resp = await self.client.get(f"{self.base_url}/api/tags", timeout=2.0)
            
            if resp.status_code == 200:
                data = resp.json()
                self.models = [
                    ModelInfo(
                        m["name"],
                        m["name"],
                        8192, # default approx
                        f"Local model: {m['name']}",
                        ["local"]
                    ) for m in data.get("models", [])
                ]
                self.status = "connected"
        except Exception:
            self.status = "error"
            
    async def test_connection(self) -> Tuple[bool, float, str]:
        start = time.time()
        try:
            resp = await self.client.get(self.base_url)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self.status = "connected"
                return True, latency, ""
            return False, latency, f"HTTP {resp.status_code}"
        except httpx.RequestError as e:
            self.status = "disconnected"
            return False, 0.0, f"Connection failed: {str(e)}"
            
    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": True
        }
        
        async with self.client.stream("POST", url, json=payload, timeout=None) as response:
            if response.status_code != 200:
                err = await response.aread()
                raise ValueError(f"Ollama error: {err.decode('utf-8')}")
                
            async for line in response.aiter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
                except json.JSONDecodeError:
                    continue

    async def chat(self, model_id: str, messages: List[dict]) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": False
        }
        
        resp = await self.client.post(url, json=payload, timeout=None)
        if resp.status_code != 200:
            raise ValueError(f"Ollama error: {resp.text}")
        
        data = resp.json()
        return data["message"]["content"]
