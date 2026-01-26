"""
Planner Agent - Responsible for planning and structuring the test case.
"""
from tenacity import retry, stop_after_attempt, wait_exponential
from src.env import env_variables

from openai import Client

from src.models.test_case import TestCaseModel
from src.tools.clients.gen_ia_client import GenIAClient


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_test_case_refactor(client: Client, prompt: str) -> TestCaseModel | None:
    """
    Restructure and refactor a test case using LLM with structured output.
    
    This agent takes a prompt containing test case information and uses
    OpenAI's structured output parsing to generate a properly formatted
    TestCaseModel object.
    
    Args:
        client: OpenAI client instance (will be overridden by GenIAClient).
        prompt: The system prompt containing test case restructuring instructions.
        
    Returns:
        TestCaseModel with the restructured test case, or None if parsing fails.
        
    Raises:
        Exception: After 3 retry attempts with exponential backoff.
    """
    client = GenIAClient.get_client()
    
    completion = client.beta.chat.completions.parse(
        model=env_variables.ai_agent_model,
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        response_format=TestCaseModel,
        temperature=0.1,
        n=1,
    )
    
    return completion.choices[0].message.parsed
