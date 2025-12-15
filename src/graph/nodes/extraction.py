"""
Extraction node (Level 2) - Extracts HTML elements from pages.
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


async def extraction_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for extracting HTML elements from pages (Level 2).
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with extracted elements
    """
    logger.info("Starting element extraction...")
    
    module_idx = state["current_module_index"]
    test_plan = state["test_plan"]
    
    if module_idx >= len(test_plan.modules):
        state["execution_status"] = "coding"
        return state
    
    current_module = test_plan.modules[module_idx]
    logger.info(f"Processing module {module_idx + 1}/{len(test_plan.modules)}: {current_module.url}")
    
    templates_dir = Path(__file__).parent.parent.parent / "prompts"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("level2_extraction.jinja2")
    
    module_dict = current_module.model_dump()
    prompt = template.render(module=json.dumps(module_dict, indent=2))
    
    api_key = get_api_key()
    async with BrowserTool(api_key) as browser:
        result = await browser.extract_elements(
            url=current_module.url,
            instruction=prompt,
            schema=ExtractedElement.model_json_schema(),
            temperature=0.0
        )
    
    module_dict["extracted_data"] = result["extracted_content"]
    module_dict["token"] = result["token_usage"]
    module_dict["dispatcher"] = result["dispatcher_data"]
    
    module_dict = map_extracted_data_to_steps(module_dict)
    
    test_plan.modules[module_idx] = type(current_module)(**module_dict)
    
    state["messages"].append({
        "role": "assistant",
        "content": f"Elements extracted from module {module_idx + 1}",
        "node": "extraction"
    })
    
    state["execution_status"] = "refining"
    
    logger.info(f"Extraction completed for module {module_idx + 1}")
    
    return state
