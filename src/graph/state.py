"""
Shared state for the LangGraph workflow for E2E test generation.
"""
from typing import TypedDict, List, Optional, Annotated, Dict, Any
from langgraph.graph.message import add_messages, BaseMessage
from src.models import TestCaseModel
from src.models.extracted_test_case_model import ExtractedTestCaseModel
from src.utils.enums import GenIAStateStatus

class GenIAState(TypedDict):
    """
    Main state of the LangGraph graph.
    
    This state is shared across all graph nodes and maintains
    information about the progress of E2E test generation.
    """
    # Messages exchanged between agents
    messages: Annotated[List[BaseMessage], add_messages]
    
    
    # Workflow execution status
    execution_status: GenIAStateStatus
    
    # Current attempt number to process the input
    attempt_number: int
    
    # Initial user input (raw test case text)
    test_case: str
    
    # Original test case name (filename without extension)
    test_case_name: str
    
    # Output directory for final test script
    output_directory: str

    # Current module index being processed in TestCaseModel
    current_module_index: int
    
    
    # TestCaseModel extracted from initial prompt by LLM (Level 1 output)
    refined_test_case: Optional[TestCaseModel]
    

    # Test case data after extraction (Level 2 first pass)
    extracted_test_case: Optional[ExtractedTestCaseModel]
    
    # Test case data after refinement (Level 2 second pass)
    refined_extracted_test_case: Optional[ExtractedTestCaseModel]
    
    
    # Robot Framework script generated at end of workflow (Level 3 output)
    script_robot: Optional[str]

