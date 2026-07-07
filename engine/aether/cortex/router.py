from typing import Dict, Any, List
from aether.cortex.graph import CortexGraph
from aether.cortex.nodes.analytical import AnalyticalNode
from aether.cortex.nodes.creative import CreativeNode

class AdaptiveRouter:
    """
    Analyzes incoming tasks and routes them through the optimal computation graph.
    """
    def __init__(self, graph: CortexGraph):
        self.graph = graph
        
        # Initialize default nodes
        self.analytical = AnalyticalNode(node_id="analytical_primary")
        self.creative = CreativeNode(node_id="creative_primary")
        
        self.graph.add_node(self.analytical)
        self.graph.add_node(self.creative)
        
    async def route_task(self, query: str) -> Dict[str, Any]:
        """
        Determine the best execution pathway for a given query.
        """
        context = {"query": query}
        results = {}
        
        # Very rudimentary task analysis heuristic
        lower_query = query.lower()
        needs_analysis = any(word in lower_query for word in ["calculate", "analyze", "why", "how", "code", "logic"])
        needs_creative = any(word in lower_query for word in ["imagine", "brainstorm", "create", "story", "design"])
        
        # If ambiguous, use both
        if not needs_analysis and not needs_creative:
            needs_analysis = True
            needs_creative = True
            
        # Execute determined pathway
        if needs_analysis:
            results["analytical"] = await self.analytical.process(context)
            
        if needs_creative:
            # Pass analytical context if both run (chaining)
            if needs_analysis:
                context["analytical_prior"] = results["analytical"]
                # Form/strengthen pathway
                self.graph.add_pathway(self.analytical.id, self.creative.id)
                self.graph.update_pathway_weight(self.analytical.id, self.creative.id, 0.1)
                
            results["creative"] = await self.creative.process(context)
            
        return results
