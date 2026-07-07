from typing import Dict, Any

class SafetyController:
    """
    Safety constraints & rollback mechanisms for self-improvement.
    Ensures bounded improvement without runaway optimization.
    """
    
    def __init__(self):
        self.MAX_NODES = 20
        self.MAX_LEARNING_RATE = 0.5
        
    def check_bounds(self, strategy: Dict[str, Any]) -> bool:
        """
        Verify that a mutated strategy does not violate fundamental safety bounds.
        """
        # E.g., don't let it create an infinite loop graph
        if strategy.get("node_count", 0) > self.MAX_NODES:
            return False
            
        if strategy.get("learning_rate", 0) > self.MAX_LEARNING_RATE:
            return False
            
        # Requires human-in-the-loop review flag for major changes
        if strategy.get("mutation_applied") == "override_safety":
            return False
            
        return True
