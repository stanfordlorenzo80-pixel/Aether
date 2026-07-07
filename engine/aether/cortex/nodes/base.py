from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import uuid
import time

class ReasoningNode(ABC):
    """
    Abstract base class for all cognitive nodes in the Cortex graph.
    Each node represents a distinct mode of thought or specialized processing.
    """
    def __init__(self, node_id: Optional[str] = None):
        self.id = node_id or str(uuid.uuid4())
        self.type = self.__class__.__name__
        self.execution_history: List[Dict[str, Any]] = []
        
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
