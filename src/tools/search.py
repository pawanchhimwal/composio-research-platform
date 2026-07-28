"""Web Search Tool to locate official developer documentation."""
import os
from tavily import TavilyClient
from config.settings import settings
from utils.logger import get_logger

logger = get_logger()

class WebSearcher:
    def __init__(self):
        self.api_key = settings.SEARCH_API_KEY
        if not self.api_key or self.api_key == "your-search-api-key-here":
            logger.warning("SEARCH_API_KEY is not configured properly. Search might fail.")
            self.client = None
        else:
            self.client = TavilyClient(api_key=self.api_key)

    def search_docs(self, app_name: str) -> list[str]:
        """Search for the official developer documentation and API reference."""
        if not self.client:
            # Fallback mock for testing if no API key is provided
            return [
                f"https://developer.{app_name.lower().replace(' ', '')}.com/docs",
                f"https://api.{app_name.lower().replace(' ', '')}.com/reference"
            ]

        query = f'"{app_name}" official developer documentation API reference authentication'
        logger.debug(f"Searching for docs: {query}")
        
        try:
            response = self.client.search(query=query, search_depth="basic", max_results=3)
            urls = [result['url'] for result in response.get('results', [])]
            return urls
        except Exception as e:
            logger.error(f"Failed to search for {app_name}: {e}")
            return []
