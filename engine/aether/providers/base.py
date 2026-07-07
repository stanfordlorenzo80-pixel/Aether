from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator, Tuple

class ModelInfo:
    def __init__(self, id: str, name: str, context_window: int, description: str = "", capabilities: List[str] = None):
        self.id = id
        self.name = name
        self.context_window = context_window
        self.description = description
        self.capabilities = capabilities or []

class BaseProvider(ABC):
    def __init__(self, id: str, name: str, ptype: str):
        self.id = id
        self.name = name
        self.type = ptype  # 'cloud' or 'local'
        self.status = "disconnected"
        self.models: List[ModelInfo] = []
        
    @abstractmethod
    async def initialize(self):
        pass
        
    @abstractmethod
    async def test_connection(self) -> Tuple[bool, float, str]:
        """Returns (success, latency_ms, error_msg)"""
        pass
        
    @abstractmethod
    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        pass
        
    def get_info(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "models": [
                {
                    "id": m.id,
                    "name": m.name,
                    "contextWindow": m.context_window,
                    "description": m.description,
                    "capabilities": m.capabilities
                } for m in self.models
            ]
        }
