"""
Planner Agent - Responsible for planning and structuring the test case.
"""
from src.graph.nodes.restructuring import restructuring_node
from src.graph.state import GenIAState


class PlannerAgent:
    """
    Agent responsible for planning test case execution.
    
    This agent analyzes the test case in natural language and converts it
    into a modular structure organized by URLs.
    """
    
    def __init__(self):
        self.name = "Planner"
    
    def execute(self, state: GenIAState) -> GenIAState:
        """
        Executes test case planning.
        
        Args:
            state: Current state of the graph
            
        Returns:
            Updated state
        """
        return restructuring_node(state)
