import math
from typing import Dict, Any, List

def calculate_phi(graph_state: Dict[str, Any], active_pathways: List[Dict[str, Any]]) -> float:
    """
    Calculates a heuristic approximation of Integrated Information (Φ).
    In IIT, Φ measures how much the system is 'more than the sum of its parts'.
    For our computation graph, it measures the interdependency of reasoning nodes.
    
    Args:
        graph_state: State of nodes in the graph
        active_pathways: Connections between nodes with their weights
        
    Returns:
        float: Φ score (0.0 to 1.0) representing coherence/integration
    """
    if not active_pathways:
        return 0.0
        
    # Heuristic: highly interconnected nodes with strong bidirectional 
    # weights yield higher Φ. Isolated components reduce Φ.
    
    total_weight = sum(p.get("weight", 0) for p in active_pathways)
    num_nodes = len(graph_state.get("nodes", []))
    
    if num_nodes <= 1:
        return 0.0
        
    # Simulated calculation for the framework foundation
    integration = total_weight / (num_nodes * (num_nodes - 1))
    
    # Sigmoid normalization to 0-1
    phi = 1 / (1 + math.exp(-10 * (integration - 0.5)))
    return round(phi, 4)
