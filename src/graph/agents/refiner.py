"""
Refiner Agent - Responsible for refining extracted HTML elements.
"""
from typing import Any, Dict

from playwright._impl._errors import TargetClosedError
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.models import ExtractedElement
from src.tools.browser import BrowserTool
from src.utils.logger import get_logger

logger = get_logger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=15),
    retry=retry_if_not_exception_type(TargetClosedError),
)
async def refine_extracted_elements(
    url: str,
    instruction: str,
) -> Dict[str, Any]:
    """
    Refine previously extracted HTML elements for accuracy.
    
    Args:
        url: The URL to re-analyze for element refinement.
        instruction: LLM instruction for refinement.
        
    Returns:
        Dictionary containing:
            - extracted_content: List of refined elements
            - token_usage: Token usage statistics
            - dispatcher_data: Dispatcher performance data
    """
    logger.info(f"Refining elements for: {url}")
    
    async with BrowserTool() as browser:
        result = await browser.extract_elements(
            url=url,
            instruction=instruction,
            schema=ExtractedElement.model_json_schema(),
            temperature=0.0
        )
    
    logger.info(f"Refinement completed for: {url}")
    
    return result
