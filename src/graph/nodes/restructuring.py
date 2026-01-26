"""
Restructuring node (Level 1) - Converts test case into structured modules.
"""
from langchain_core.messages import AIMessage

from src.graph.agents.test_refactor import generate_test_case_refactor
from src.graph.state import GenIAState
from src.tools.files import load_prompt
from src.utils.enums import GenIAStateStatus
from src.utils.logger import get_logger
from src.tools.clients.gen_ia_client import GenIAClient

logger = get_logger(__name__)


def restructuring_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for analyzing test case and breaking it into modules (Level 1).
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with refined_test_case filled
    """
    logger.info("Starting test case restructuring...")
    
    state["execution_status"] = GenIAStateStatus.RESTRUCTURING
    
    prompt = load_prompt(
        "agents/langgraph/level1_restructuring.jinja2",
        test_case=state["test_case"]
    )
    
    refined_test_case = generate_test_case_refactor(
        client=GenIAClient.get_client(),
        prompt=prompt
    )
    
    if refined_test_case is None:
        raise ValueError("Failed to restructure test case - LLM returned None")
    
    state["refined_test_case"] = refined_test_case
    state["current_module_index"] = 0
    
    new_message = AIMessage(
        content=f"Test case restructured with {len(refined_test_case.modules)} modules",
        name="restructuring",
    )
    
    state["messages"].append(new_message)
    
    logger.info(f"Test case restructured successfully: {len(refined_test_case.modules)} modules")
    
    return state
