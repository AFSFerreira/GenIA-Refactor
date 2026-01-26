"""
Explorer Agent - Responsible for extracting HTML elements from web pages.
"""
from typing import Any, Dict, List

from playwright._impl._errors import TargetClosedError
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.env import env_variables
from src.models import ExtractedElement
from src.tools.browser import BrowserTool
from src.utils.logger import get_logger

logger = get_logger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=15),
    retry=retry_if_not_exception_type(TargetClosedError),
)
async def extract_elements_from_page(
    url: str,
    instruction: str,
) -> Dict[str, Any]:
    """
    Extract HTML elements from a web page using LLM-based extraction.
    
    Args:
        url: The URL to crawl and extract elements from.
        instruction: LLM instruction for extraction.
        
    Returns:
        Dictionary containing:
            - extracted_content: List of extracted elements
            - token_usage: Token usage statistics
            - dispatcher_data: Dispatcher performance data
    """
    logger.info(f"Extracting elements from: {url}")
    
    async with BrowserTool() as browser:
        result = await browser.extract_elements(
            url=url,
            instruction=instruction,
            schema=ExtractedElement.model_json_schema(),
            temperature=0.0
        )
    
    logger.info(f"Extraction completed for: {url}")
    
    return result
