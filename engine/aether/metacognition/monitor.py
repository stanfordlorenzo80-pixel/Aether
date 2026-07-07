from typing import Dict, Any, List
import time

class MetaMonitor:
    """
    Real-time observation of reasoning quality, confidence, and coherence.
    Watches the Cortex graph execute and logs anomalies or sub-optimal pathways.
    """
    def __init__(self):
        self.observations: List[Dict[str, Any]] = []
        
    def observe_execution(self, query: str, pathway_results: Dict[str, Any], phi_score: float):
        """
        Record a snapshot of how the system reasoned through a task.
        """
        # Determine overall confidence based on node outputs
        node_confidences = []
        for node_id, result in pathway_results.items():
            if "confidence" in result:
                node_confidences.append(result["confidence"])
                
        avg_confidence = sum(node_confidences) / len(node_confidences) if node_confidences else 0.0
        
        observation = {
            "timestamp": time.time(),
            "query_length": len(query),
            "nodes_activated": list(pathway_results.keys()),
            "phi_score": phi_score,
            "avg_confidence": avg_confidence,
            "anomaly_detected": avg_confidence < 0.5 or phi_score < 0.2
        }
        
        self.observations.append(observation)
        return observation
        
    def get_recent_anomalies(self) -> List[Dict[str, Any]]:
        return [obs for obs in self.observations[-10:] if obs.get("anomaly_detected")]
