"""
Represents an execution step in the test case.
"""
from pydantic import BaseModel, Field
from typing import List
from src.models.extracted_element import ExtractedElement


class ExecutionStepModel(BaseModel):
    """Represents an execution step in the test case."""
    step: str = Field(
        ..., 
        description="A description of the user action or verification performed on this page."
    )
    extracted_data: List[ExtractedElement] = Field(
        default_factory=list,
        description="List of HTML elements involved in this step. Can be empty if not applicable."
    )
