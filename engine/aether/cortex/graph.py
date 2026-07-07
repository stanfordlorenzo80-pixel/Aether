import networkx as nx
from typing import Dict, Any, List
from aether.cortex.nodes.base import ReasoningNode

class CortexGraph:
    """
    Manages the adaptive computation DAG (Directed Acyclic Graph).
    Nodes are instances of ReasoningNode.
    Edges represent pathways with weights and activation history.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_map: Dict[str, ReasoningNode] = {}
        
    def add_node(self, node: ReasoningNode):
        if node.id not in self.nodes_map:
            self.nodes_map[node.id] = node
            self.graph.add_node(node.id, type=node.type)
            
    def add_pathway(self, source_id: str, target_id: str, initial_weight: float = 1.0):
        if source_id in self.nodes_map and target_id in self.nodes_map:
            self.graph.add_edge(source_id, target_id, weight=initial_weight, activations=0)
            
    def update_pathway_weight(self, source_id: str, target_id: str, delta: float):
        if self.graph.has_edge(source_id, target_id):
            current_weight = self.graph[source_id][target_id]['weight']
            # Sigmoid bounded weight update between 0.1 and 10.0
            new_weight = max(0.1, min(10.0, current_weight + delta))
            self.graph[source_id][target_id]['weight'] = new_weight
            self.graph[source_id][target_id]['activations'] += 1
            
    def get_state(self) -> Dict[str, Any]:
        """Serialize current graph state for monitoring and metrics"""
        return {
            "nodes": list(self.nodes_map.keys()),
            "edges": list(self.graph.edges(data=True)),
            "node_types": {nid: node.type for nid, node in self.nodes_map.items()}
        }
