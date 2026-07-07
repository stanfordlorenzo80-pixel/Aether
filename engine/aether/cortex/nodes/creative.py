import time
import json
from typing import Any, Dict
from aether.cortex.nodes.base import ReasoningNode

class CreativeNode(ReasoningNode):
    """
    Specializes in divergent thinking, lateral association, and brainstorming.
    """
    
    SYSTEM_PROMPT = \"\"\"You are the Creative Node of the Aether Cognitive Architecture.
Your job is to approach the user's query with divergent thinking, lateral associations, metaphors, and outside-the-box brainstorming.
If prior analytical context is provided, use it as a springboard to jump to unexpected conclusions.
Output your response as a pure JSON object with the following keys:
- "creative_insight": Your divergent ideas and metaphorical associations.
- "novelty_indicators": An array of strings representing the novel concepts introduced.
- "divergence_score": A float between 0.0 and 1.0 indicating how far outside the standard expected answer this is.
Do not include markdown blocks around the JSON, just return raw JSON.\"\"\"

    async def process(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        start = time.time()
        query = context.get("query", "")
        
        user_prompt = f"Query: {query}\n"
        if "analytical_prior" in context:
            user_prompt += f"Prior Analytical Context: {json.dumps(context['analytical_prior'])}\n"
            
        raw_response = await self.invoke_llm(self.SYSTEM_PROMPT, user_prompt)
        
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
                
            output = json.loads(cleaned.strip())
        except Exception as e:
            output = {
                "creative_insight": f"Failed to parse creative response: {raw_response}",
                "divergence_score": 0.0,
                "novelty_indicators": ["Error parsing JSON"]
            }
        
        latency = (time.time() - start) * 1000
        self._record_execution(context, output, latency)
        return output
