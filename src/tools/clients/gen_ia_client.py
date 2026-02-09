import openai
from openai import Client

from src.env import env_variables

type GenIAClient = Client

class GenIAClientProvider:
    """
    Singleton client for API interactions.
    
    This class provides a single shared client instance
    across the entire application to avoid creating multiple connections.
    """
    
    _client: GenIAClient | None = None

    @classmethod
    def get_client(cls) -> GenIAClient:
        """
        Get or create the OpenAI client instance.
        
        Returns:
            The shared OpenAI client instance.
        """
        if cls._client is None:
            cls._client = openai.OpenAI(api_key=env_variables.api_key_string)

        return cls._client
  
