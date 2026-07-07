from typing import Dict, Any, List
import math

class PathwayManager:
    """
    Manages the formation, strengthening, and pruning of reasoning pathways.
    Inspired by Hebbian learning (neuroplasticity).
    """
    def __init__(self, decay_rate: float = 0.05, learning_rate: float = 0.1):
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate
        
    def reinforce_pathway(self, success_score: float) -> float:
        """
        Calculate weight delta based on success score.
        Success score > 0.5 leads to positive delta (strengthening).
        Success score < 0.5 leads to negative delta (weakening).
        """
        # Normalize score around 0
        normalized = (success_score - 0.5) * 2.0
        delta = normalized * self.learning_rate
        return delta
        
    def prune_pathways(self, edges_data: List[tuple]) -> List[tuple]:
        """
        Identify pathways that should be pruned due to low weight or inactivity.
        Returns list of (source, target) tuples to prune.
        """
        to_prune = []
        for source, target, data in edges_data:
            weight = data.get('weight', 1.0)
            activations = data.get('activations', 0)
            
            # If weight falls below threshold and hasn't been active
            if weight < 0.2 and activations < 5:
                to_prune.append((source, target))
                
        return to_prune
