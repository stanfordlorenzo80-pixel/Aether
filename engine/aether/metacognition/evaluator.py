from typing import Dict, Any
import json

class PerformanceEvaluator:
    """
    Performance self-assessment against task objectives.
    Uses an LLM-as-a-Judge pipeline to determine how well a reasoning pathway answered the query.
    """
    def __init__(self, registry):
        self.registry = registry
        self.SYSTEM_PROMPT = \"\"\"You are the Aether Performance Evaluator.
Analyze the user query and the system's reasoning output. Score the output on a scale of 0.0 to 1.0 based on:
1. Accuracy and Relevance
2. Depth of Reasoning
3. Logical Coherence
Output pure JSON:
{"score": float, "critique": "short explanation"}
Do not use markdown blocks.\"\"\"
    
    async def evaluate(self, query: str, output: Dict[str, Any]) -> float:
        user_prompt = f"Query: {query}\nOutput: {json.dumps(output)}\n"
        
        try:
            # Fallback to claude-haiku if available, else first model
            p_info = self.registry.get_all_providers_info()
            if not p_info or not p_info[0]["models"]:
                return 0.5
            
            pid = p_info[0]["id"]
            mid = p_info[0]["models"][0]["id"]
            if pid == "claude":
                mid = "claude-3-haiku-20240307"
                
            raw_response = await self.registry.chat(pid, mid, [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ])
            
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"): cleaned = cleaned[7:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            
            evaluation = json.loads(cleaned.strip())
            return float(evaluation.get("score", 0.5))
        except Exception:
            return 0.5
