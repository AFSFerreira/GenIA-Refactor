from typing import Optional

from pydantic import BaseModel

# NOTE: Adicionar 'Field' posteriormente:
class DispatcherStatsModel(BaseModel):
    memory_usage_MB: float = 0.0
    duration_seconds: float = 0.0
    memory_usage_MB: float = 0.0
    peak_memory_MB: float = 0.0
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: float = 0.0
