"""
Code generation node (Level 3) - Generates Robot Framework script.
"""
from src.graph.state import GenIAState
from src.utils.config import get_openai_client
from src.utils.logger import get_logger
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json

logger = get_logger(__name__)


def generation_node(state: GenIAState) -> GenIAState:
    """
    Node responsible for generating Robot Framework script (Level 3).
    
    Args:
        state: Current state of the graph
        
    Returns:
        State updated with generated script_robot
    """
    logger.info("Starting Robot Framework script generation...")
    
    # Load Jinja2 template
    templates_dir = Path(__file__).parent.parent.parent / "prompts"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("level3_generation.jinja2")
    
    # Convert test_plan to dict
    test_case_dict = state["test_plan"].model_dump()
    
    # Render prompt
    prompt = template.render(
        test_case_with_extracted_data=json.dumps(test_case_dict, indent=2)
    )
    
    # Generate script using OpenAI
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a skilled test automation engineer. Your task is to guide the user in creating an end-to-end (E2E) test script using Python, Robot Framework, and Selenium based on the provided test case and list of JSON objects."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    # Extract generated script
    robot_script = response.choices[0].message.content
    
    # Update state
    state["script_robot"] = robot_script
    state["execution_status"] = "finished"
    
    # Add message to history
    state["messages"].append({
        "role": "assistant",
        "content": "Robot Framework script generated successfully",
        "node": "generation"
    })
    
    logger.info("Robot Framework script generated successfully")
    
    return state
