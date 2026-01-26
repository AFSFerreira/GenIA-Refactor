"""
Extraction node (Level 2) - Extracts HTML elements from pages using crawl4ai.
"""
import json
from langchain_core.messages import AIMessage

from src.graph.agents.explorer import extract_elements_from_page
from src.graph.state import GenIAState
from src.tools.file_system import map_extracted_data_to_steps
from src.tools.files import load_prompt
from src.utils.enums import GenIAStateStatus
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def extraction_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for extracting HTML elements from pages (Level 2 - First Pass).
    
    This node iterates through each module in the refined test case,
    visits the corresponding URL, and extracts relevant HTML elements
    needed to execute the test steps.
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with extracted elements for current module
    """
    logger.info("Starting element extraction...")
    
    state["execution_status"] = GenIAStateStatus.EXPLORING
    
    refined_test_case = state["refined_test_case"]
    
    if refined_test_case is None:
        raise ValueError("refined_test_case is required for extraction")
    
    module_idx = state["current_module_index"]
    total_modules = len(refined_test_case.modules)
    
    # Check if all modules have been processed
    if module_idx >= total_modules:
        logger.info("All modules extracted, moving to coding phase")
        state["execution_status"] = GenIAStateStatus.CODING
        return state
    
    # Initialize extracted_test_case if not present
    if state.get("extracted_test_case") is None:
        state["extracted_test_case"] = refined_test_case.model_dump()
    
    # Initialize refined_extracted_test_case if not present
    if state.get("refined_extracted_test_case") is None:
        state["refined_extracted_test_case"] = refined_test_case.model_dump()
    
    current_module = refined_test_case.modules[module_idx]
    logger.info(f"Processing module {module_idx + 1}/{total_modules}: {current_module.url}")
    
    # Load extraction prompt template
    prompt = load_prompt(
        "agents/langgraph/level2_extraction.jinja2",
        module=json.dumps(current_module.model_dump(), indent=2)
    )
    
    # Extract elements using explorer agent
    result = await extract_elements_from_page(
        url=current_module.url,
        instruction=prompt
    )
    
    # Update extracted_test_case with results
    extracted_test_case = state["extracted_test_case"]
    
    if extracted_test_case is None:
        raise ValueError("extracted_test_case should have been initialized")
    
    extracted_test_case["modules"][module_idx]["extracted_data"] = result["extracted_content"]
    extracted_test_case["modules"][module_idx]["token"] = result["token_usage"]
    extracted_test_case["modules"][module_idx]["dispatcher"] = result["dispatcher_data"]
    
    # Map extracted data to execution steps
    extracted_test_case["modules"][module_idx] = map_extracted_data_to_steps(
        extracted_test_case["modules"][module_idx]
    )
    
    state["extracted_test_case"] = extracted_test_case
    
    # Transition to refinement phase
    state["execution_status"] = GenIAStateStatus.REFINING
    
    new_message = AIMessage(
        content=f"Elements extracted from module {module_idx + 1}/{total_modules}: {current_module.url}",
        name="extraction",
    )
    state["messages"].append(new_message)
    
    logger.info(f"Extraction completed for module {module_idx + 1}")
    
    return state
