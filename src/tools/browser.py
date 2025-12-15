"""
Tools for browser interaction using Crawl4AI.
"""
from crawl4ai import (
    AsyncWebCrawler, 
    BrowserConfig, 
    CrawlerRunConfig, 
    CacheMode, 
    LLMConfig,
    MemoryAdaptiveDispatcher
)
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from typing import Dict, Any, Optional
from datetime import datetime
import json


class BrowserTool:
    """Tool for navigation and element extraction with Crawl4AI."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.crawler: Optional[AsyncWebCrawler] = None
        self.dispatcher = MemoryAdaptiveDispatcher()
    
    async def __aenter__(self):
        """Initializes the crawler."""
        self.crawler = AsyncWebCrawler()
        await self.crawler.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the crawler."""
        if self.crawler:
            await self.crawler.__aexit__(exc_type, exc_val, exc_tb)
    
    async def extract_elements(
        self,
        url: str,
        instruction: str,
        schema: Dict[str, Any],
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        """
        Extracts HTML elements from a URL using LLM.
        
        Args:
            url: URL of the page to be analyzed
            instruction: Instruction for the LLM about what to extract
            schema: JSON schema for validating extracted data
            temperature: Temperature for the LLM
            
        Returns:
            Dict containing extracted_content, token_usage and dispatcher_data
        """
        llm_strategy = LLMExtractionStrategy(
            llm_config=LLMConfig(
                provider="openai/gpt-4o-mini",
                api_token=self.api_key
            ),
            schema=schema,
            extraction_type="schema",
            input_format="html",
            extra_args={"temperature": temperature},
            instruction=instruction
        )
        
        browser_cfg = BrowserConfig(headless=True)
        
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
        
        result_data = {}
        
        for result in results:
            if result.success:
                # Extracted data
                result_data["extracted_content"] = json.loads(result.extracted_content)
                
                # Tokens used
                usage = llm_strategy.total_usage
                result_data["token_usage"] = {
                    "completion_tokens": usage.completion_tokens,
                    "prompt_tokens": usage.prompt_tokens,
                    "total_tokens": usage.total_tokens,
                    "completion_tokens_details": usage.completion_tokens_details,
                    "prompt_tokens_details": usage.prompt_tokens_details
                }
                
                # Dispatcher data
                start_time = datetime.fromtimestamp(result.dispatch_result.start_time)
                end_time = datetime.fromtimestamp(result.dispatch_result.end_time)
                result_data["dispatcher_data"] = {
                    "memory_usage_MB": result.dispatch_result.memory_usage,
                    "peak_memory_MB": result.dispatch_result.peak_memory,
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "duration_seconds": (end_time - start_time).total_seconds()
                }
        
        return result_data
