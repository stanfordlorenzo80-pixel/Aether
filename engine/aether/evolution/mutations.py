from typing import Dict, Any, List
import copy
import json

class MutationEngine:
    """
    Generates variations of successful strategies (DSPy style).
    Uses the LLM to rewrite and optimize the internal system prompts of nodes.
    """
    def __init__(self, registry):
        self.registry = registry
        self.SYSTEM_PROMPT = \"\"\"You are the Aether Mutation Engine.
Your task is to take an existing system prompt and a performance critique, and generate 3 improved, mutated variants of the prompt.
Output pure JSON:
{"mutations": [{"mutation_applied": "type", "new_prompt": "..."}]}
Do not use markdown blocks.\"\"\"
    
    async def generate_variants(self, base_strategy: Dict[str, Any], critique: str, n: int = 3) -> List[Dict[str, Any]]:
        current_prompt = base_strategy.get("system_prompt", "")
        if not current_prompt: return []
        
        user_prompt = f"Current Prompt: {current_prompt}\nCritique: {critique}"
        
        try:
            p_info = self.registry.get_all_providers_info()
            if not p_info: return []
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
            
            data = json.loads(cleaned.strip())
            
            variants = []
            for i, mut in enumerate(data.get("mutations", [])[:n]):
                variant = copy.deepcopy(base_strategy)
                variant["id"] = f"{base_strategy.get('id', 'base')}_mut_{i}"
                variant["mutation_applied"] = mut.get("mutation_applied", "unknown")
                variant["system_prompt"] = mut.get("new_prompt", current_prompt)
                variants.append(variant)
            return variants
        except Exception:
            return []
