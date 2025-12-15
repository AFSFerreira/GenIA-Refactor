"""
Represents a complete test case.
"""
from pydantic import BaseModel, Field
from typing import List
from src.models.module import ModuleModel


class TestCaseModel(BaseModel):
    """Represents a complete test case."""
    testCase: str = Field(
        ..., 
        description="Test Case Name"
    )
    modules: List[ModuleModel] = Field(
        ..., 
        description="A list of modules representing separate URLs involved in the test case."
    )
