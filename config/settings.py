"""Global configuration management via environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
    MODEL = os.getenv("MODEL", "gpt-4o")
    
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "./data/outputs")
    CHECKPOINT_FILE = os.path.join(OUTPUT_FOLDER, "checkpoint.json")
    
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    CONFIDENCE_THRESHOLD = 0.8  # Below this requires human review

settings = Settings()
