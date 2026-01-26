"""
Shared state for the LangGraph workflow for E2E test generation.
"""
from typing import TypedDict, List, Optional, Annotated, Dict, Any
from langgraph.graph.message import add_messages, BaseMessage
from src.models import TestCaseModel
from src.utils.enums import GenIAStateStatus

class GenIAState(TypedDict):
    """
    Main state of the LangGraph graph.
    
    This state is shared across all graph nodes and maintains
    information about the progress of E2E test generation.
    """
    # Messages exchanged between agents
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Number of agent attempts to process input
    attempt_number: Optional[int]
    
    # Initial user input (raw test case text)
    test_case: str
    
    # Original test case name (filename without extension)
    test_case_name: Optional[str]
    
    # TestCaseModel extracted from initial prompt by LLM (Level 1 output)
    refined_test_case: Optional[TestCaseModel]
    
    # Current module index being processed in TestCaseModel
    current_module_index: int
    
    # Workflow execution status
    execution_status: Optional[GenIAStateStatus]
    
    # Output directory for final test script
    output_directory: Optional[str]
    
    # Robot Framework script generated at end of workflow (Level 3 output)
    script_robot: Optional[str]
    
    # Test case data after extraction (Level 2 first pass)
    extracted_test_case: Optional[Dict[str, Any]]
    
    # Test case data after refinement (Level 2 second pass)
    refined_extracted_test_case: Optional[Dict[str, Any]]
    
    # Crawler instance for browser operations (shared across extraction/refinement)
    crawler_context: Optional[Any]

