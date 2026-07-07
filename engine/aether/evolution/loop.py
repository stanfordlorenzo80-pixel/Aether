import time
from typing import Dict, Any, List
from aether.evolution.safety import SafetyController
from aether.evolution.mutations import MutationEngine
from aether.evolution.selection import SelectionEngine

class EvolutionLoop:
    """
    Core self-improvement loop for Aether.
    Safely orchestrates the generation, evaluation, and selection of new reasoning strategies.
    """
    def __init__(self):
        self.safety = SafetyController()
        self.mutator = MutationEngine()
        self.selector = SelectionEngine()
        self.is_running = False
        self.generation = 1
        
    async def run_epoch(self, current_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run one generation of the self-improvement loop.
        """
        self.is_running = True
        
        # 1. Mutate
        candidates = self.mutator.generate_variants(current_strategy, n=3)
        
        # 2. Evaluate in sandbox
        evaluated_candidates = []
        for candidate in candidates:
            # Check safety bounds before running
            if not self.safety.check_bounds(candidate):
                continue
                
            score = await self.selector.evaluate_fitness(candidate)
            candidate["fitness"] = score
            evaluated_candidates.append(candidate)
            
        # 3. Select best
        best_candidate = self.selector.select_best(current_strategy, evaluated_candidates)
        
        self.generation += 1
        self.is_running = False
        
        return best_candidate
