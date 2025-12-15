"""
Pydantic models for test case data structuring.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractedElement(BaseModel):
    """Represents an HTML element extracted from a page."""
    type: str = Field(
        ..., 
        description="Specifies the HTML element type. Example: 'input', 'button', 'select', etc."
    )
    request_description: str = Field(
        ..., 
        description="A detailed explanation of what the element asks from the user. Example: 'Enter your First Name'."
    )
    identifier_type: str = Field(
        ..., 
        description="The method used to locate the HTML element. Preferably 'XPath', but can be ID, name, or other unique identifiers."
    )
    identifier_tracking: str = Field(
        ..., 
        description="The exact path or unique identifier to locate the HTML element. For XPath, ensure it's the full and correct path. Example: '//*[@id=\"root\"]/div/div[2]/div/form/input[2]'."
    )
    step_name: str = Field(
        ..., 
        description="Indicates which test case step utilizes this element during execution"
    )


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


class ModuleModel(BaseModel):
    """Represents a test module (a specific URL)."""
    url: str = Field(
        ..., 
        description="The specific URL where this portion of the test case is executed. Must include protocol (e.g., 'https://')."
    )
    purpose: str = Field(
        ..., 
        description="A brief and clear description of the main objective for this URL in the test case."
    )
    execution_steps: List[ExecutionStepModel] = Field(
        ..., 
        description="A list of step objects that detail user actions and extracted elements on this page."
    )


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
