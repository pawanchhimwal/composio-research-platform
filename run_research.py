#!/usr/bin/env python3
"""Entry point for the Composio Research Agent pipeline."""
import os
import sys

# Ensure the src directory is on the path if needed, though running from root works.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.orchestrator import Orchestrator
from config.settings import settings

def main():
    data_file = os.path.join("data", "apps_master.csv")
    output_file = os.path.join(settings.OUTPUT_FOLDER, "results.json")
    checkpoint_file = settings.CHECKPOINT_FILE
    
    orchestrator = Orchestrator(
        data_file=data_file,
        output_file=output_file,
        checkpoint_file=checkpoint_file
    )
    
    orchestrator.run()

if __name__ == "__main__":
    main()
