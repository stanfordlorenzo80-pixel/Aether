import json
from typing import Dict, Any, List
from aether.cortex.graph import CortexGraph
from aether.cortex.nodes.analytical import AnalyticalNode
from aether.cortex.nodes.creative import CreativeNode

class AdaptiveRouter:
    """
    Analyzes incoming tasks and routes them through the optimal computation graph using an LLM.
    """
    def __init__(self, graph: CortexGraph, registry):
        self.graph = graph
        self.registry = registry
        
        # Initialize default nodes with registry
        self.analytical = AnalyticalNode(registry=registry, node_id="analytical_primary")
        self.creative = CreativeNode(registry=registry, node_id="creative_primary")
        
        self.graph.add_node(self.analytical)
        self.graph.add_node(self.creative)
        
    async def route_task(self, query: str) -> Dict[str, Any]:
        """
        Determine the best execution pathway for a given query using LLM classification.
        """
        system_prompt = \"\"\"You are the Aether Routing mechanism.
Analyze the user's query and decide which cognitive nodes should process it.
Respond in pure JSON format:
{
  "needs_analytical": boolean, // True if the query requires logic, coding, math, or step-by-step breakdown
  "needs_creative": boolean // True if the query requires brainstorming, lateral thinking, or narrative
}
Do not wrap in markdown.\"\"\"

        try:
            # We'll use the registry directly
            # Fallback to claude-haiku if available, else first model
            p_info = self.registry.get_all_providers_info()
            if not p_info or not p_info[0]["models"]:
                raise ValueError("No models available")
            
            pid = p_info[0]["id"]
            mid = p_info[0]["models"][0]["id"]
            # prefer claude haiku for speed if claude is active
            if pid == "claude":
                mid = "claude-3-haiku-20240307"
                
            raw_response = await self.registry.chat(pid, mid, [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ])
            
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            decision = json.loads(cleaned.strip())
            needs_analytical = decision.get("needs_analytical", True)
            needs_creative = decision.get("needs_creative", True)
        except Exception:
            # Fallback if classification fails
            needs_analytical = True
            needs_creative = True

        context = {"query": query}
        results = {}
            
        # Execute determined pathway
        if needs_analytical:
            results["analytical"] = await self.analytical.process(context)
            
        if needs_creative:
            # Pass analytical context if both run (chaining)
            if needs_analytical:
                context["analytical_prior"] = results["analytical"]
                # Form/strengthen pathway
                self.graph.add_pathway(self.analytical.id, self.creative.id)
                self.graph.update_pathway_weight(self.analytical.id, self.creative.id, 0.1)
                
            results["creative"] = await self.creative.process(context)
            
        return results
