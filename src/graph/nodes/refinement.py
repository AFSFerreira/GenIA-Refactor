"""
Refinement node (Level 2) - Refines and validates extracted elements.
"""
import json
from langchain_core.messages import AIMessage

from src.graph.agents.refiner import refine_extracted_elements
from src.graph.state import GenIAState
from src.models.extracted_module_model import ExtractedModuleModel
from src.models.extraction_result import ExtractionResultModel
from src.tools.load_prompt import load_prompt
from src.tools.parser import map_extracted_data_to_steps
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
    
    refined_test_case = state.get("refined_test_case")
    extracted_test_case = state.get("extracted_test_case")
    
    if refined_test_case is None:
        raise ValueError("refined_test_case is required for refinement")
    
    if extracted_test_case is None:
        raise ValueError("extracted_test_case is required for refinement")
    
    module_idx = state["current_module_index"]
    total_modules = len(refined_test_case.modules)
    
    refined_extracted_test_case = state.get("refined_extracted_test_case")
    
    if refined_extracted_test_case is None:
        raise ValueError("refined_extracted_test_case is required for refinement")

    current_module_extracted = refined_extracted_test_case.modules[module_idx]
    
    logger.info(f"Refining module {module_idx + 1}/{total_modules}: {current_module_extracted.url}")
    
    # Load refinement prompt template
    prompt = load_prompt(
        "agents/langgraph/level2_refinement.jinja2",
        module_with_extracted_data=json.dumps(
            current_module_extracted.model_dump(exclude_none=True, mode='json'), 
            indent=2
        )
    )
    
    # Refine elements using refiner agent
    refinement_result: ExtractionResultModel = await refine_extracted_elements(
        url=current_module_extracted.url,
        instruction=prompt
    )
    
    current_module_extracted.token = refinement_result.token_usage
    current_module_extracted.dispatcher = refinement_result.dispatcher_data
    
    # Map extracted data to execution steps
    current_module_extracted = map_extracted_data_to_steps(
        module_model=current_module_extracted,
        extracted_elements=refinement_result.extracted_content
    )
    
    refined_extracted_test_case.modules[module_idx] = current_module_extracted
    
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
        content=f"Elements refined for module {module_idx + 1}/{total_modules}: {current_module_extracted.url}",
        name="refinement",
    )
    
    state["messages"].append(new_message)
    
    logger.info(f"Refinement completed for module {module_idx + 1}")
    
    return state
