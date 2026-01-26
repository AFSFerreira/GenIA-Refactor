import openai
from openai import Client

from src.env import env_variables

class GenIAClient:
  _client: Client
  
  @classmethod
  def get_client(cls) -> Client:
    if cls._client is None:
      cls._client = openai.OpenAI(api_key=env_variables.api_key_string)
    
    return cls._client
  
