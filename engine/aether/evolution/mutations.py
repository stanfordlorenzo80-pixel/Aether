from typing import Dict, Any, List
import copy
import random

class MutationEngine:
    """
    Generates variations of successful strategies.
    (e.g. prompt engineering, pathway topology changes)
    """
    
    def generate_variants(self, base_strategy: Dict[str, Any], n: int = 3) -> List[Dict[str, Any]]:
        variants = []
        for i in range(n):
            variant = copy.deepcopy(base_strategy)
            variant["id"] = f"{base_strategy.get('id', 'base')}_mut_{i}"
            
            # Simulated mutations
            mutation_type = random.choice(["tweak_weights", "add_node", "remove_node"])
            variant["mutation_applied"] = mutation_type
            
            if mutation_type == "tweak_weights":
                variant["learning_rate"] = variant.get("learning_rate", 0.1) * random.uniform(0.8, 1.2)
                
            variants.append(variant)
            
        return variants
