from typing import Optional

from src.models.dispatcher_stats import DispatcherStatsModel
from src.models.module import ModuleModel
from src.models.token_usage import TokenUsageModel


# NOTE: Adicionar 'Field' posteriormente:
class ExtractedModuleModel(ModuleModel):
    token: Optional[TokenUsageModel] = None
    dispatcher: Optional[DispatcherStatsModel] = None
