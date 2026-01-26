"""
Coder Agent - Responsible for generating Robot Framework scripts.
"""
from tenacity import retry, stop_after_attempt, wait_exponential

from src.env import env_variables
from src.tools.clients.gen_ia_client import GenIAClient
from src.utils.logger import get_logger

logger = get_logger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_robot_script(prompt: str) -> str:
    """
    Generate Robot Framework script from test case data.
    
    Args:
        prompt: The prompt containing test case data and instructions.
        
    Returns:
        Generated Robot Framework script content.
        
    Raises:
        ValueError: If LLM returns empty response.
    """
    logger.info("Generating Robot Framework script...")
    
    client = GenIAClient.get_client()
    
    response = client.chat.completions.create(
        model=env_variables.ai_agent_model,
        messages=[
            {
                "role": "system",
                "content": "You are a skilled test automation engineer. Your task is to create an end-to-end (E2E) test script using Python, Robot Framework, and Selenium based on the provided test case and list of JSON objects."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        n=1,
        temperature=0.1,
    )
    
    robot_script = response.choices[0].message.content
    
    if robot_script is None:
        raise ValueError("LLM returned empty response for Robot Framework script")
    
    # Clean up markdown code blocks if present
    if robot_script.startswith("```"):
        lines = robot_script.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        robot_script = "\n".join(lines)
    
    logger.info("Robot Framework script generated successfully")
    return robot_script
