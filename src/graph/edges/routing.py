"""
Decision functions for conditional edges of the graph.
"""
from src.graph.state import GenIAState


def should_continue_extraction(state: GenIAState) -> str:
    """
    Decides whether to continue extracting or finish.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Name of the next node
    """
    status = state["execution_status"]
    
    if status == "extracting":
        return "extraction"
    elif status == "refining":
        return "refinement"
    elif status == "coding":
        return "generation"
    elif status == "finished":
        return "end"
    else:
        return "end"


def route_after_restructuring(state: GenIAState) -> str:
    """
    Routing after restructuring.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Name of the next node
    """
    return "extraction"


def route_after_extraction(state: GenIAState) -> str:
    """
    Routing after extraction.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Name of the next node
    """
    return "refinement"


def route_after_refinement(state: GenIAState) -> str:
    """
    Routing after refinement.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Name of the next node
    """
    if state["current_module_index"] < len(state["test_plan"].modules):
        return "extraction"
    else:
        return "generation"


def route_after_generation(state: GenIAState) -> str:
    """
    Routing after generation.
    
    Args:
        state: Current state of the graph
        
    Returns:
        Name of the next node
    """
    
    return "end"
