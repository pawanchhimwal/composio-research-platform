"""Validates evidence URLs by checking reachability and domain authority."""
import requests
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.logger import get_logger

logger = get_logger()

class EvidenceValidator:
    def __init__(self):
        self.headers = {
            "User-Agent": "Composio-Verification-Agent/1.0"
        }

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=3))
    def check_url_reachable(self, url: str) -> bool:
        """Checks if a URL returns a 200/300 status code."""
        if not url:
            return False
        try:
            # We use GET because some sites block HEAD requests
            response = requests.get(url, headers=self.headers, timeout=5, stream=True)
            return response.status_code < 400
        except requests.exceptions.RequestException as e:
            logger.debug(f"URL validation failed for {url}: {e}")
            return False

    def is_official_domain(self, target_url: str, app_website: str) -> bool:
        """Checks if the evidence URL belongs to the official app domain or known doc hubs."""
        if not target_url or not app_website:
            return False
            
        try:
            target_domain = urlparse(target_url).netloc.lower()
            website_domain = urlparse(app_website).netloc.lower()
            
            # Remove www.
            target_domain = target_domain.replace("www.", "")
            website_domain = website_domain.replace("www.", "")
            
            # Match base domain
            base_website = ".".join(website_domain.split('.')[-2:])
            
            if base_website in target_domain:
                return True
                
            # Allow known trusted doc hubs like github, readme, stoplight etc.
            trusted_hubs = ["github.com", "readme.io", "stoplight.io", "gitbook.io"]
            for hub in trusted_hubs:
                if hub in target_domain:
                    return True
                    
            return False
        except Exception:
            return False

    def validate_evidence(self, url: str, app_website: str) -> dict:
        """Performs full validation on an evidence URL."""
        reachable = self.check_url_reachable(url)
        official = self.is_official_domain(url, app_website)
        
        return {
            "reachable": reachable,
            "official": official,
            "valid": reachable and official
        }
