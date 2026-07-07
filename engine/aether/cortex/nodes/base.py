from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import uuid
import time

class ReasoningNode(ABC):
    """
    Abstract base class for all cognitive nodes in the Cortex graph.
    Each node represents a distinct mode of thought or specialized processing.
    """
    def __init__(self, registry, node_id: Optional[str] = None):
        self.id = node_id or str(uuid.uuid4())
        self.type = self.__class__.__name__
        self.registry = registry
        self.execution_history: List[Dict[str, Any]] = []
        
    async def invoke_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Helper to call the active LLM via the registry"""
        # Defaulting to Claude Haiku for internal reasoning speed if available
        # In a real setup, this would be configurable per-node
        try:
            return await self.registry.chat(
                provider_id="claude",
                model_id="claude-3-haiku-20240307",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
        except Exception:
            # Fallback to first available model if Claude fails
            providers = self.registry.get_all_providers_info()
            if not providers:
                return "Error: No LLM providers available."
            p = providers[0]
            if not p["models"]:
                return "Error: No models available."
            return await self.registry.chat(p["id"], p["models"][0]["id"], [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ])

    @abstractmethod
    async def process(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Process the input context and return the node's output contribution.
        """
        pass
        
    def _record_execution(self, input_context: Dict[str, Any], output: Dict[str, Any], latency: float):
        self.execution_history.append({
            "timestamp": time.time(),
            "latency_ms": latency,
            "input_keys": list(input_context.keys()),
            "output_keys": list(output.keys())
        })
