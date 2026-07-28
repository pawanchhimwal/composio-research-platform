"""Centralized structured logging."""
import sys
import os
from loguru import logger
from datetime import datetime
from config.settings import settings

# Ensure log directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a run-specific log file
run_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = os.path.join(LOG_DIR, f"run_{run_time}.log")

# Configure logger
logger.remove()  # Remove default handler
logger.add(sys.stdout, level=settings.LOG_LEVEL, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")
logger.add(log_file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}")

def get_logger():
    return logger
