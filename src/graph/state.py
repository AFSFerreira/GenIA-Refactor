"""
Shared state for the LangGraph workflow for E2E test generation.
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages
from src.models import TestCaseModel, ModuleModel


class GenIAState(TypedDict):
    """
    Main state of the LangGraph graph.
    
    This state is shared across all graph nodes and maintains
    information about the progress of E2E test generation.
    """
    messages: Annotated[List[dict], add_messages]
    test_plan: Optional[TestCaseModel]
    current_module_index: int
    execution_status: str
    script_robot: Optional[str]
    test_case_name: Optional[str]
    output_directory: Optional[str]
    attempt_number: Optional[int]
