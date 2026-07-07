from typing import Dict, Any, List

class LearningPlanner:
    """
    Autonomous decisions about what reasoning strategies to try next.
    Takes observations from the MetaMonitor and generates mutation targets.
    """
    def __init__(self):
        self.strategy_queue: List[Dict[str, Any]] = []
        
    def plan_next_strategies(self, recent_anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        If we see anomalies (low confidence, low phi), plan a new routing strategy.
        """
        plans = []
        if recent_anomalies:
            # E.g. we struggled with analytical tasks recently.
            # Plan: Try injecting a 'critical critique' node into the analytical pathway.
            plans.append({
                "action": "mutate_pathway",
                "target": "analytical_primary",
                "mutation": "append_critical_node"
            })
            
        self.strategy_queue.extend(plans)
        return plans
