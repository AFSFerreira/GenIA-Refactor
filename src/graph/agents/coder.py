"""
Coder Agent - Responsible for generating Robot Framework scripts.
"""
from tenacity import retry, stop_after_attempt, wait_exponential

from src.env import env_variables
from src.env.index import EnvironmentVariables
from src.tools.clients.gen_ia_client import GenIAClient, GenIAClientProvider
from src.tools.parser import strip_markdown_code_fences
from src.utils.logger import get_logger

logger = get_logger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_robot_script(client: GenIAClient, prompt: str) -> str:
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
    
    response = client.chat.completions.create(
        model=env_variables.ai_agent_model,
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        temperature=EnvironmentVariables.ai_agents_temperature,
        n=EnvironmentVariables.ai_agents_responses_quantity,
    )
    
    robot_script = response.choices[0].message.content
    
    if robot_script is None:
        raise ValueError("LLM returned empty response for Robot Framework script")
    
    # Clean up markdown code blocks if present
    robot_script = strip_markdown_code_fences(robot_script)
    
    logger.info("Robot Framework script generated successfully")
    
    return robot_script
