from typing import List

from pydantic import Field
from src.models import TestCaseModel
from src.models.extracted_module_model import ExtractedModuleModel

class ExtractedTestCaseModel(TestCaseModel):
    modules: List[ExtractedModuleModel] = Field(
        ..., 
        description=""
    )
