"""
Global application configuration.
"""
import os
from dotenv import load_dotenv
import openai
from pathlib import Path

# Load environment variables
load_dotenv()


def get_api_key() -> str:
    """
    Gets the OpenAI API key.
    
    Returns:
        API key
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    return api_key


def get_openai_client() -> openai.OpenAI:
    """
    Creates an OpenAI client.
    
    Returns:
        Configured OpenAI client
    """
    return openai.OpenAI(api_key=get_api_key())


def get_test_case_file() -> str:
    """
    Gets the test case file path from environment variable.
    
    Returns:
        Path to the test case file or None
    """
    return os.getenv("TEST_CASE")


def get_example_folder() -> Path:
    """
    Gets the path to the examples folder.
    
    Returns:
        Path to TestCaseExamples folder
    """
    return Path('TestCaseExamples')


def get_output_folder() -> Path:
    """
    Gets the path to the output folder.
    
    Returns:
        Path to TestCases folder
    """
    return Path('TestCases')


# Model configurations
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE_EXTRACTION = 0.0
TEMPERATURE_REFINEMENT = 0.0
TEMPERATURE_GENERATION = 0.0

# Crawl4AI configurations
BROWSER_HEADLESS = True
WORD_COUNT_THRESHOLD = 1
