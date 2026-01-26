"""Helpers for loading required environment variables used across the project."""

from dataclasses import dataclass
import os
from dotenv import load_dotenv
from pathlib import Path
from openai.types import ChatModel

@dataclass
class EnvironmentVariables:
  """Strongly-typed container for the environment variables this project needs."""
  test_case_file: str
  api_key_string: str
  langgraph_agents_prompts_dir: Path = Path('..', 'prompts', 'agents', 'langgraph')
  test_cases_examples_folder: Path = Path('..', '..', 'TestCaseExamples')
  test_cases_output_folder: Path = Path('..', '..', 'TestCases')
  ai_agent_model: ChatModel = "gpt-4o-mini"

class MissingConfigurationError(Exception):
    """Raised when a required environment variable is missing."""
    def __init__(self, variable_name: str):
      super().__init__(f"The required environment variable '{variable_name}' was not set.")

load_dotenv()

def get_env_variables() -> EnvironmentVariables:
  """Load and validate required environment variables, raising if any are absent."""
  test_case_file = os.getenv("TEST_CASE")
  
  if test_case_file == None:
    raise MissingConfigurationError("test_case_file")

  api_key_string = os.getenv("OPENAI_API_KEY")
  
  if api_key_string == None:
    raise MissingConfigurationError("api_key_string")
  
  return EnvironmentVariables(test_case_file=test_case_file, api_key_string=api_key_string)

env_variables = get_env_variables()
