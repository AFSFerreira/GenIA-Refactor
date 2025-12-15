"""
Configuration and construction of the LangGraph graph.
"""
from langgraph.graph import StateGraph, END
from src.graph.state import GenIAState
from src.graph.nodes import (
    restructuring_node,
    extraction_node,
    refinement_node,
    generation_node
)
from src.graph.edges import (
    route_after_restructuring,
    route_after_extraction,
    route_after_refinement,
    route_after_generation
)


def create_workflow() -> StateGraph:
    """
    Creates the LangGraph workflow.
    
    Returns:
        Configured StateGraph
    """
    workflow = StateGraph(GenIAState)
    
    workflow.add_node("restructuring", restructuring_node)
    workflow.add_node("extraction", extraction_node)
    workflow.add_node("refinement", refinement_node)
    workflow.add_node("generation", generation_node)
    
    workflow.set_entry_point("restructuring")
    
    workflow.add_conditional_edges(
        "restructuring",
        route_after_restructuring,
        {
            "extraction": "extraction"
        }
    )
    
    workflow.add_conditional_edges(
        "extraction",
        route_after_extraction,
        {
            "refinement": "refinement"
        }
    )
    
    workflow.add_conditional_edges(
        "refinement",
        route_after_refinement,
        {
            "extraction": "extraction",
            "generation": "generation"
        }
    )
    
    workflow.add_conditional_edges(
        "generation",
        route_after_generation,
        {
            "end": END
        }
    )
    
    return workflow


def compile_workflow() -> StateGraph:
    """
    Compiles the workflow for execution.
    
    Returns:
        Compiled workflow
    """
    workflow = create_workflow()
    return workflow.compile()
