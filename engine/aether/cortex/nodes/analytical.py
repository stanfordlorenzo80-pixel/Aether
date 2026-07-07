import time
import json
from typing import Any, Dict
from aether.cortex.nodes.base import ReasoningNode

class AnalyticalNode(ReasoningNode):
    """
    Specializes in formal logic, step-by-step breakdowns, math, and code analysis.
    """
    
    SYSTEM_PROMPT = \"\"\"You are the Analytical Node of the Aether Cognitive Architecture.
Your job is to break down the user's query using formal logic, step-by-step reasoning, and structural analysis.
Output your response as a pure JSON object with the following keys:
- "analytical_insight": A detailed, logical breakdown of the problem.
- "reasoning_trace": An array of strings detailing the logical steps you took.
- "confidence": A float between 0.0 and 1.0 indicating how confident you are in this analysis.
Do not include markdown blocks around the JSON, just return raw JSON.\"\"\"

    async def process(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        start = time.time()
        query = context.get("query", "")
        
        raw_response = await self.invoke_llm(self.SYSTEM_PROMPT, query)
        
        try:
            # Clean potential markdown formatting
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
                
            output = json.loads(cleaned.strip())
        except Exception as e:
            output = {
                "analytical_insight": f"Failed to parse analytical response: {raw_response}",
                "confidence": 0.0,
                "reasoning_trace": ["Error parsing JSON"]
            }
        
        latency = (time.time() - start) * 1000
        self._record_execution(context, output, latency)
        return output
