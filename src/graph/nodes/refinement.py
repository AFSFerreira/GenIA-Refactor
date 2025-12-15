"""
Refinement node (Level 2) - Refines and validates extracted elements.
"""
from src.graph.state import GenIAState
from src.models import ExtractedElement
from src.tools.browser import BrowserTool
from src.tools.file_system import map_extracted_data_to_steps
from src.utils.config import get_api_key
from src.utils.logger import get_logger
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json

logger = get_logger(__name__)


async def refinement_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for refining extracted HTML elements (Level 2).
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with refined elements
    """
    logger.info("Starting element refinement...")
    
    module_idx = state["current_module_index"]
    test_plan = state["test_plan"]
    current_module = test_plan.modules[module_idx]
    
    logger.info(f"Refining module {module_idx + 1}/{len(test_plan.modules)}")
    
    templates_dir = Path(__file__).parent.parent.parent / "prompts"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("level2_refinement.jinja2")
    
    module_dict = current_module.model_dump()
    prompt = template.render(module_with_extracted_data=json.dumps(module_dict, indent=2))
    
    api_key = get_api_key()
    async with BrowserTool(api_key) as browser:
        result = await browser.extract_elements(
            url=current_module.url,
            instruction=prompt,
            schema=ExtractedElement.model_json_schema(),
            temperature=0.0
        )
    
    # Update module with refined data
    module_dict["extracted_data"] = result["extracted_content"]
    if "token" in module_dict:
        for key in result["token_usage"]:
            if key in module_dict["token"]:
                if isinstance(module_dict["token"][key], (int, float)):
                    module_dict["token"][key] += result["token_usage"][key]
    else:
        module_dict["token"] = result["token_usage"]
    
    module_dict["dispatcher_refinement"] = result["dispatcher_data"]
    
    module_dict = map_extracted_data_to_steps(module_dict)
    
    test_plan.modules[module_idx] = type(current_module)(**module_dict)
    
    state["messages"].append({
        "role": "assistant",
        "content": f"Elements refined for module {module_idx + 1}",
        "node": "refinement"
    })
    
    state["current_module_index"] += 1
    if state["current_module_index"] >= len(test_plan.modules):
        state["execution_status"] = "coding"
    else:
        state["execution_status"] = "extracting"
    
    logger.info(f"Refinement completed for module {module_idx + 1}")
    
    return state
