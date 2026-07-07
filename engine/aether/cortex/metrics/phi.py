from typing import Dict, Any, List
import json

class PhiCalculator:
    def __init__(self, registry):
        self.registry = registry
        self.SYSTEM_PROMPT = \"\"\"You are the Aether Information Integration Evaluator.
Given the reasoning graph state and the outputs of the nodes, calculate a Causal Coherence Score (Phi).
Measure how deeply interconnected and mutually dependent the node outputs are.
Output pure JSON:
{"phi_score": float, "analysis": "short explanation"}
Do not use markdown blocks.\"\"\"

    async def calculate_phi(self, graph_state: Dict[str, Any], active_pathways: List[Dict[str, Any]], outputs: Dict[str, Any]) -> float:
        if not active_pathways:
            return 0.0
            
        user_prompt = f"Graph: {json.dumps(graph_state)}\nPathways: {json.dumps(active_pathways)}\nOutputs: {json.dumps(outputs)}"
        
        try:
            p_info = self.registry.get_all_providers_info()
            if not p_info or not p_info[0]["models"]: return 0.0
            
            pid = p_info[0]["id"]
            mid = p_info[0]["models"][0]["id"]
            if pid == "claude": mid = "claude-3-haiku-20240307"
                
            raw_response = await self.registry.chat(pid, mid, [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ])
            
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            
            evaluation = json.loads(cleaned.strip())
            return float(evaluation.get("phi_score", 0.0))
        except Exception:
            return 0.0
