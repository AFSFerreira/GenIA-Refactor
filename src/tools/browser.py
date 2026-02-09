"""
Browser tool for web crawling and element extraction using crawl4ai.
"""
import asyncio
import json
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Union

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
    """Singleton manager for the browser crawler instance."""
    _instance: ClassVar[Optional["BrowserManager"]] = None
    _crawler: Optional[AsyncWebCrawler] = None
    _lock: ClassVar[asyncio.Lock] = asyncio.Lock()
    _in_use: bool = False
    
    def __new__(cls) -> "BrowserManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def get_crawler(self) -> AsyncWebCrawler:
        async with self._lock:
            if self._crawler is None:
                logger.info("Creating new AsyncWebCrawler instance")
                browser_config = BrowserConfig(headless=True)
                self._crawler = AsyncWebCrawler(config=browser_config)
                await self._crawler.__aenter__()
            self._in_use = True
            return self._crawler
    
    async def release(self) -> None:
        async with self._lock:
            self._in_use = False
    
    async def close(self) -> None:
        async with self._lock:
            if self._crawler is not None and not self._in_use:
                logger.info("Closing AsyncWebCrawler instance")
                try:
                    await self._crawler.__aexit__(None, None, None)
                except Exception as e:
                    logger.warning(f"Error closing crawler: {e}")
                finally:
                    self._crawler = None

_browser_manager = BrowserManager()


class BrowserTool:
    """Tool for extracting HTML elements from web pages using LLM-based extraction."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or env_variables.api_key_string
        self.crawler: Optional[AsyncWebCrawler] = None
        self.dispatcher = MemoryAdaptiveDispatcher()
    
    async def __aenter__(self):
        self.crawler = await _browser_manager.get_crawler()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await _browser_manager.release()
    
    async def extract_elements(
        self,
        url: str,
        instruction: str,
        schema: Dict[str, Any],
        temperature: float = 0.0,
        model: str = "openai/gpt-4o-mini"
    ) -> Dict[str, Any]:
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
            input_format="markdown", 
            extra_args={"temperature": temperature},
            instruction=instruction
        )
        
        crawl_config = CrawlerRunConfig(
            verbose=True,
            word_count_threshold=1,
            extraction_strategy=llm_strategy,
            cache_mode=CacheMode.BYPASS,
            # Opcional: Adicionar espera para carregamento de JS
            wait_for="body" 
        )
        
        results = await self.crawler.arun_many(
            urls=[url],
            config=crawl_config,
            dispatcher=self.dispatcher
        )
        
        print("\n\n\n\n")
        print(results)
        print("\n\n\n\n")
        
        extracted_content: List[Dict[str, Any]] = []
        token_usage: Dict[str, Any] = {
            "completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0
        }
        dispatcher_data: Dict[str, Any] = {}
        
        result_list: List[Any] = []
        
        if isinstance(results, list):
            result_list = results
        
        elif hasattr(results, '__aiter__'):
            async for r in results: # type: ignore[union-attr]
                result_list.append(r)
        else:
            result_list = [results]
        
        for result in result_list:
            if result.success:
                logger.debug(f"Extraction successful for {url}")
                
                try:
                    raw_content = json.loads(result.extracted_content)
                    
                    print("\n\n\n\n")
                    print(raw_content)
                    print("\n\n\n\n")
                    
                    if isinstance(raw_content, list):
                        extracted_content = raw_content
                    elif isinstance(raw_content, dict):
                        found_list = False
                        for key, value in raw_content.items():
                            if isinstance(value, list):
                                extracted_content = value
                                found_list = True
                                break
                        
                        if not found_list:
                            extracted_content = [raw_content]
                    else:
                        extracted_content = []
                        
                except Exception as e:
                    logger.error(f"Failed to parse JSON content: {e}")
                    extracted_content = []
            else:
                error_msg = result.error_message or "Unknown error"
                
                if "playwright install" in error_msg or "Executable doesn't exist" in error_msg:
                    logger.critical("🚨 PLAYWRIGHT BROWSERS MISSING! Run 'playwright install' in your terminal.")
                    raise RuntimeError(f"Critical Crawler Failure: {error_msg}")
                
                logger.warning(f"Extraction failed for {url}. Error: {error_msg}")
                
        return {
            "extracted_content": extracted_content,
            "token_usage": token_usage,
            "dispatcher_data": dispatcher_data
        }
