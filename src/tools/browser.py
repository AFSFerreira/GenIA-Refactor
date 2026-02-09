"""
Browser tool for web crawling and element extraction using crawl4ai.
"""
import asyncio
import json
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMConfig,
    MemoryAdaptiveDispatcher,
)
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from src.env import env_variables
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BrowserManager:
    """
    Singleton manager for the browser crawler instance.
    
    Ensures only one AsyncWebCrawler instance is used throughout the application.
    """
    
    _instance: ClassVar[Optional["BrowserManager"]] = None
    _crawler: Optional[AsyncWebCrawler] = None
    _lock: ClassVar[asyncio.Lock] = asyncio.Lock()
    _in_use: bool = False
    
    def __new__(cls) -> "BrowserManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_crawler(self) -> AsyncWebCrawler:
        """Get the shared crawler instance, creating it if needed."""
        async with self._lock:
            if self._crawler is None:
                logger.info("Creating new AsyncWebCrawler instance")
                browser_config = BrowserConfig(headless=True)
                self._crawler = AsyncWebCrawler(config=browser_config)
                await self._crawler.__aenter__()
            self._in_use = True
            return self._crawler
    
    async def release(self) -> None:
        """Release reference to the crawler."""
        async with self._lock:
            self._in_use = False
    
    async def close(self) -> None:
        """Close the crawler if not in use."""
        async with self._lock:
            if self._crawler is not None and not self._in_use:
                logger.info("Closing AsyncWebCrawler instance")
                try:
                    await self._crawler.__aexit__(None, None, None)
                except Exception as e:
                    logger.warning(f"Error closing crawler: {e}")
                finally:
                    self._crawler = None


# Global browser manager instance
_browser_manager = BrowserManager()


class BrowserTool:
    """
    Tool for extracting HTML elements from web pages using LLM-based extraction.
    
    Uses crawl4ai to navigate pages and extract structured data based on
    provided instructions and schemas.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the browser tool.
        
        Args:
            api_key: OpenAI API key. If not provided, uses environment variable.
        """
        self.api_key = api_key or env_variables.api_key_string
        self.crawler: Optional[AsyncWebCrawler] = None
        self.dispatcher = MemoryAdaptiveDispatcher()
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.crawler = await _browser_manager.get_crawler()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await _browser_manager.release()
    
    async def extract_elements(
        self,
        url: str,
        instruction: str,
        schema: Dict[str, Any],
        temperature: float = 0.0,
        model: str = "openai/gpt-4o-mini"
    ) -> Dict[str, Any]:
        """
        Extract HTML elements from a URL based on the provided instruction.
        
        Args:
            url: The URL to crawl and extract elements from.
            instruction: LLM instruction for extraction.
            schema: JSON schema for the expected output format.
            temperature: LLM temperature setting.
            model: LLM model to use for extraction.
            
        Returns:
            Dictionary containing:
                - extracted_content: List of extracted elements
                - token_usage: Token usage statistics
                - dispatcher_data: Dispatcher performance data
        """
        if not self.crawler:
            raise RuntimeError("BrowserTool must be used as async context manager")
        
        logger.info(f"Extracting elements from: {url}")
        
        llm_strategy = LLMExtractionStrategy(
            llm_config=LLMConfig(
                provider=model,
                api_token=self.api_key
            ),
            schema=schema,
            extraction_type="schema",
            input_format="html",
            extra_args={"temperature": temperature},
            instruction=instruction
        )
        
        crawl_config = CrawlerRunConfig(
            verbose=True,
            word_count_threshold=1,
            extraction_strategy=llm_strategy,
            cache_mode=CacheMode.BYPASS
        )
        
        results = await self.crawler.arun_many(
            urls=[url],
            config=crawl_config,
            dispatcher=self.dispatcher
        )
        
        extracted_content: List[Dict[str, Any]] = []
        token_usage: Dict[str, Any] = {}
        dispatcher_data: Dict[str, Any] = {}
        
        # Handle results from arun_many - can be async generator or list-like
        result_list: List[Any] = []
        if hasattr(results, '__aiter__'):
            async for r in results:  # type: ignore
                result_list.append(r)
        else:
            result_list = list(results)  # type: ignore
        
        for result in result_list:
            if result.success:
                logger.debug(f"Extraction successful for {url}")
                logger.debug(f"LLM usages: {llm_strategy.usages}")
                
                extracted_content = json.loads(result.extracted_content)
                
                usage = llm_strategy.total_usage
                token_usage = {
                    "completion_tokens": usage.completion_tokens,
                    "prompt_tokens": usage.prompt_tokens,
                    "total_tokens": usage.total_tokens,
                    "completion_tokens_details": usage.completion_tokens_details,
                    "prompt_tokens_details": usage.prompt_tokens_details
                }
                
                start_time = datetime.fromtimestamp(result.dispatch_result.start_time)
                end_time = datetime.fromtimestamp(result.dispatch_result.end_time)
                dispatcher_data = {
                    "memory_usage_MB": result.dispatch_result.memory_usage,
                    "peak_memory_MB": result.dispatch_result.peak_memory,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "duration_seconds": (end_time - start_time).total_seconds()
                }
            else:
                logger.warning(f"Extraction failed for {url}")
        
        return {
            "extracted_content": extracted_content,
            "token_usage": token_usage,
            "dispatcher_data": dispatcher_data
        }
