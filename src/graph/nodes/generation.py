"""
Code generation node (Level 3) - Generates Robot Framework script.
"""
import json
from langchain_core.messages import AIMessage

from src.graph.state import GenIAState
from src.graph.agents.coder import generate_robot_script
from src.tools.clients.gen_ia_client import GenIAClientProvider
from src.tools.load_prompt import load_prompt
from src.utils.enums import GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generation_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for generating Robot Framework script (Level 3).
    
    This node takes the refined test case with all extracted elements
    and generates an executable Robot Framework E2E test script.
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with generated script_robot
    """
    logger.info("Starting Robot Framework script generation...")
    
    state["execution_status"] = GenIAStateStatus.CODING
    
    refined_extracted_test_case = state.get("refined_extracted_test_case")
    
    if refined_extracted_test_case is None:
        raise ValueError("refined_extracted_test_case is required for code generation")
    
    # Load generation prompt template
    prompt = load_prompt(
        "agents/langgraph/level3_generation.jinja2",
        test_case_with_extracted_data=refined_extracted_test_case.model_dump(exclude_none=True, mode='json'), indent=2
    )
    
    logger.info("Calling coder agent to generate Robot Framework script...")
    
    # Use the coder agent to generate the script
    robot_script = generate_robot_script(client=GenIAClientProvider.get_client(), prompt=prompt)
    
    state["script_robot"] = robot_script
    state["execution_status"] = GenIAStateStatus.FINISHED
    
    new_message = AIMessage(
        content="Robot Framework script generated successfully",
        name="generation",
    )
    state["messages"].append(new_message)
    
    logger.info("Robot Framework script generated successfully")
    
    return state
