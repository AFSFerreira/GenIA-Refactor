"""
Restructuring node (Level 1) - Converts test case into structured modules.
"""
from src.graph.state import GenIAState
from src.models import TestCaseModel
from src.utils.config import get_openai_client
from src.utils.logger import get_logger
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

logger = get_logger(__name__)


def restructuring_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for analyzing test case and breaking it into modules (Level 1).
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with test_plan filled
    """
    logger.info("Starting test case restructuring...")
    
    templates_dir = Path(__file__).parent.parent.parent / "prompts"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("level1_restructuring.jinja2")
    
    test_case_content = None
    for msg in state["messages"]:
        if msg.get("role") == "user" and "test_case_content" in msg:
            test_case_content = msg["test_case_content"]
            break
    
    if not test_case_content:
        logger.error("Test case content not found in messages")
        return state
    
    prompt = template.render(test_case=test_case_content)
    
    client = get_openai_client()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        response_format=TestCaseModel
    )
    
    test_plan = completion.choices[0].message.parsed
    state["test_plan"] = test_plan
    state["execution_status"] = "extracting"
    state["current_module_index"] = 0
    
    state["messages"].append({
        "role": "assistant",
        "content": f"Test case restructured with {len(test_plan.modules)} modules",
        "node": "restructuring"
    })
    
    logger.info(f"Test case restructured successfully: {len(test_plan.modules)} modules")
    
    return state
