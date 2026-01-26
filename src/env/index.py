"""Helpers for loading required environment variables used across the project."""

from dataclasses import dataclass, field
import os
from dotenv import load_dotenv
from pathlib import Path
from openai.types import ChatModel

# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class EnvironmentVariables:
  """Strongly-typed container for the environment variables this project needs."""
  api_key_string: str
  prompts_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "src" / "prompts")
  test_cases_examples_folder: Path = field(default_factory=lambda: PROJECT_ROOT / "TestCaseExamples")
  test_cases_output_folder: Path = field(default_factory=lambda: PROJECT_ROOT / "TestCases")
  ai_agent_model: ChatModel = "gpt-4o-mini"


class MissingConfigurationError(Exception):
    """Raised when a required environment variable is missing."""
    def __init__(self, variable_name: str):
      super().__init__(f"The required environment variable '{variable_name}' was not set.")

load_dotenv()

def get_env_variables() -> EnvironmentVariables:
  """Load and validate required environment variables, raising if any are absent."""
  api_key_string = os.getenv("OPENAI_API_KEY")
  
  if api_key_string == None:
    raise MissingConfigurationError("api_key_string")
  
  return EnvironmentVariables(api_key_string=api_key_string)

env_variables = get_env_variables()
