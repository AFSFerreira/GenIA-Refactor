"""
Explorer Agent - Responsible for exploring pages and extracting elements.
"""
from src.graph.nodes.extraction import extraction_node
from src.graph.nodes.refinement import refinement_node
from src.graph.state import GenIAState


class ExplorerAgent:
    """
    Agent responsible for exploring web pages and extracting HTML elements.
    
    This agent navigates through the test case URLs, identifies relevant
    elements and refines extracted information.
    """
    
    def __init__(self):
        self.name = "Explorer"
    
    async def extract(self, state: GenIAState) -> GenIAState:
        """
        Extracts HTML elements from a page.
        
        Args:
            state: Current state of the graph
            
        Returns:
            State updated with extracted elements
        """
        return await extraction_node(state)
    
    async def refine(self, state: GenIAState) -> GenIAState:
        """
        Refines extracted HTML elements.
        
        Args:
            state: Current state of the graph
            
        Returns:
            State updated with refined elements
        """
        return await refinement_node(state)
