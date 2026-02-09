from typing import List

from pydantic import BaseModel, Field

from src.models.dispatcher_stats import DispatcherStatsModel
from src.models.extracted_element import ExtractedElement
from src.models.token_usage import TokenUsageModel


class ExtractionResultModel(BaseModel):
    extracted_content: List[ExtractedElement] = Field(..., description="")
    token_usage: TokenUsageModel = Field(..., description="")
    dispatcher_data: DispatcherStatsModel = Field(..., description="")
