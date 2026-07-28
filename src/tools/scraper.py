"""Web Scraper Tool to extract markdown content from URLs."""
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.logger import get_logger

logger = get_logger()

class DocScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_url(self, url: str) -> str:
        """Fetch a URL and return a clean text representation of the content."""
        logger.debug(f"Scraping URL: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Simple fallback to BeautifulSoup text extraction
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            text = soup.get_text(separator='\n')
            
            # Basic cleanup
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:15000]  # Limit context length to avoid blowing up LLM tokens
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return ""

    def scrape_multiple(self, urls: list[str]) -> str:
        """Scrape multiple URLs and combine their content."""
        combined_text = ""
        for url in urls:
            content = self.fetch_url(url)
            if content:
                combined_text += f"\n\n--- Content from {url} ---\n\n{content}"
        return combined_text
