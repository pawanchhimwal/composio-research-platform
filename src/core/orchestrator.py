"""Core orchestrator managing the pipeline loop and checkpoints."""
import os
import json
import pandas as pd
from typing import Dict, Any

from src.tools.search import WebSearcher
from src.tools.scraper import DocScraper
from src.agents.research_agent import ResearchAgent
from config.schema import ApplicationIntelligence
from utils.logger import get_logger

logger = get_logger()

class Orchestrator:
    def __init__(self, data_file: str, output_file: str, checkpoint_file: str):
        self.data_file = data_file
        self.output_file = output_file
        self.checkpoint_file = checkpoint_file
        
        self.searcher = WebSearcher()
        self.scraper = DocScraper()
        self.agent = ResearchAgent()
        
        self.checkpoints = self._load_checkpoints()

    def _load_checkpoints(self) -> Dict[str, str]:
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_checkpoint(self, app_id: str, status: str):
        self.checkpoints[str(app_id)] = status
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.checkpoint_file), exist_ok=True)
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoints, f, indent=2)

    def _append_result(self, record: dict):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        # Read existing
        data = []
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        data.append(record)
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self):
        logger.info("Starting Research Orchestrator...")
        
        if not os.path.exists(self.data_file):
            logger.error(f"Input file not found: {self.data_file}")
            return
            
        df = pd.read_csv(self.data_file)
        
        for _, row in df.iterrows():
            app_id = str(row['id'])
            app_name = row['name']
            
            if self.checkpoints.get(app_id) == "COMPLETED":
                logger.info(f"Skipping {app_name} (ID: {app_id}) - Already Completed")
                continue
                
            logger.info(f"Processing App: {app_name} (ID: {app_id})")
            
            try:
                # 1. Search
                urls = self.searcher.search_docs(app_name)
                if not urls:
                    logger.warning(f"No URLs found for {app_name}. Mark for manual review.")
                    self._save_checkpoint(app_id, "MANUAL_REVIEW_NEEDED")
                    continue
                    
                # 2. Scrape
                context = self.scraper.scrape_multiple(urls)
                
                # 3. Extract
                raw_json = self.agent.extract_intelligence(
                    app_id=int(app_id),
                    app_name=app_name,
                    app_category=row['category'],
                    app_website=row['website'],
                    markdown_context=context
                )
                
                if not raw_json:
                    logger.error(f"Extraction failed for {app_name}")
                    self._save_checkpoint(app_id, "FAILED")
                    continue
                
                # 4. Validate
                # We overwrite the ID and Name just to be safe
                raw_json['id'] = int(app_id)
                raw_json['name'] = app_name
                
                try:
                    validated_app = ApplicationIntelligence(**raw_json)
                except Exception as e:
                    logger.error(f"Schema validation failed for {app_name}: {e}")
                    self._save_checkpoint(app_id, "VALIDATION_FAILED")
                    continue
                    
                # 5. Save
                self._append_result(validated_app.model_dump())
                self._save_checkpoint(app_id, "COMPLETED")
                logger.info(f"Successfully processed {app_name}")
                
            except Exception as e:
                logger.exception(f"Unexpected error processing {app_name}: {e}")
                self._save_checkpoint(app_id, "ERROR")
                
        logger.info("Orchestrator Run Finished.")
