import openai
from openai import Client

from src.env import env_variables


class GenIAClient:
    """
    Singleton client for OpenAI API interactions.
    
    This class provides a single shared OpenAI client instance
    across the entire application to avoid creating multiple connections.
    """
    
    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Get or create the OpenAI client instance.
        
        Returns:
            The shared OpenAI client instance.
        """
        if cls._client is None:
            cls._client = openai.OpenAI(api_key=env_variables.api_key_string)

        return cls._client
  
