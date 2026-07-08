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
        """Probe Ollama and pull its live model list."""
        await self._fetch_models()

    async def _fetch_models(self):
        """Fetch models from the running Ollama instance."""
        try:
            resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            if resp.status_code != 200:
                # Fallback to localhost
                self.base_url = "http://localhost:11434"
                resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            
            if resp.status_code == 200:
                data = resp.json()
                raw_models = data.get("models", [])
                self.models = [
                    ModelInfo(
                        m["name"],
                        m["name"].split(":")[0].title(),  # Pretty name
                        int(m.get("details", {}).get("parameter_size", "8192").replace("B", "").replace("K", "000").replace("M", "000000")) if isinstance(m.get("details", {}).get("parameter_size"), str) else 8192,
                        f"Local model via Ollama",
                        ["local"]
                    ) for m in raw_models
                ]
                self.status = "connected"
            else:
                self.status = "disconnected"
        except Exception:
            self.status = "disconnected"

    def set_base_url(self, url: str):
        """Hot-swap the Ollama base URL at runtime."""
        self.base_url = url.rstrip("/")

    async def test_connection(self) -> Tuple[bool, float, str]:
        start = time.time()
        try:
            resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                # Also refresh model list on successful test
                data = resp.json()
                raw_models = data.get("models", [])
                self.models = [
                    ModelInfo(
                        m["name"],
                        m["name"].split(":")[0].title(),
                        8192,
                        f"Local model via Ollama",
                        ["local"]
                    ) for m in raw_models
                ]
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

    async def shutdown(self):
        await self.client.aclose()
