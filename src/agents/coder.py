"""
Coder Agent - Responsible for generating Robot Framework code.
"""
from src.graph.nodes.generation import generation_node
from src.graph.state import GenIAState


class CoderAgent:
    """
    Agent responsible for generating Robot Framework scripts.
    
    This agent receives structured modules with extracted elements
    and generates executable Robot Framework code.
    """
    
    def __init__(self):
        self.name = "Coder"
    
    def execute(self, state: GenIAState) -> GenIAState:
        """
        Generates the Robot Framework script.
        
        Args:
            state: Current state of the graph
            
        Returns:
            State updated with generated script
        """
        return generation_node(state)
