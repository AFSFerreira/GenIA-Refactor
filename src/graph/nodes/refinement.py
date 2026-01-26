"""
Refinement node (Level 2) - Refines and validates extracted elements.
"""
import json
from langchain_core.messages import AIMessage

from src.graph.agents.refiner import refine_extracted_elements
from src.graph.state import GenIAState
from src.tools.file_system import map_extracted_data_to_steps
from src.tools.files import load_prompt
from src.utils.enums import GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def refinement_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for refining extracted HTML elements (Level 2 - Second Pass).
    
    This node takes the extracted elements from the extraction phase and
    validates/improves the XPaths and element identifiers to ensure
    they are robust and accurate.
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with refined elements for current module
    """
    logger.info("Starting element refinement...")
    
    state["execution_status"] = GenIAStateStatus.REFINING
    
    refined_test_case = state["refined_test_case"]
    extracted_test_case = state["extracted_test_case"]
    
    if refined_test_case is None:
        raise ValueError("refined_test_case is required for refinement")
    
    if extracted_test_case is None:
        raise ValueError("extracted_test_case is required for refinement")
    
    module_idx = state["current_module_index"]
    total_modules = len(refined_test_case.modules)
    
    current_module = refined_test_case.modules[module_idx]
    module_with_extracted = extracted_test_case["modules"][module_idx]
    
    logger.info(f"Refining module {module_idx + 1}/{total_modules}: {current_module.url}")
    
    # Load refinement prompt template
    prompt = load_prompt(
        "agents/langgraph/level2_refinement.jinja2",
        module_with_extracted_data=json.dumps(module_with_extracted, indent=2)
    )
    
    # Refine elements using refiner agent
    result = await refine_extracted_elements(
        url=current_module.url,
        instruction=prompt
    )
    
    # Update refined_extracted_test_case with results
    refined_extracted_test_case = state["refined_extracted_test_case"]
    
    if refined_extracted_test_case is None:
        raise ValueError("refined_extracted_test_case should have been initialized")
    
    refined_extracted_test_case["modules"][module_idx]["extracted_data"] = result["extracted_content"]
    refined_extracted_test_case["modules"][module_idx]["token"] = result["token_usage"]
    refined_extracted_test_case["modules"][module_idx]["dispatcher"] = result["dispatcher_data"]
    
    # Map extracted data to execution steps
    refined_extracted_test_case["modules"][module_idx] = map_extracted_data_to_steps(
        refined_extracted_test_case["modules"][module_idx]
    )
    
    state["refined_extracted_test_case"] = refined_extracted_test_case
    
    # Move to next module
    state["current_module_index"] = module_idx + 1
    
    # Check if there are more modules to process
    if state["current_module_index"] >= total_modules:
        logger.info("All modules refined, moving to coding phase")
        state["execution_status"] = GenIAStateStatus.CODING
    else:
        # Go back to extraction for next module
        state["execution_status"] = GenIAStateStatus.EXPLORING
    
    new_message = AIMessage(
        content=f"Elements refined for module {module_idx + 1}/{total_modules}: {current_module.url}",
        name="refinement",
    )
    state["messages"].append(new_message)
    
    logger.info(f"Refinement completed for module {module_idx + 1}")
    
    return state
