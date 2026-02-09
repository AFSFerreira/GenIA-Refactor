from pydantic import BaseModel

# NOTE: Adicionar 'Field' posteriormente:
class TokenUsageModel(BaseModel):
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
