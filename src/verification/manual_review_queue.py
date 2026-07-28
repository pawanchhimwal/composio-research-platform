"""Manages the manual review queue for uncertain applications."""
import json
import os
from utils.logger import get_logger

logger = get_logger()

class ManualReviewQueue:
    def __init__(self, queue_file: str):
        self.queue_file = queue_file

    def flag_for_review(self, app_id: int, app_name: str, reasons: list[str]):
        """Flags an application for manual human review."""
        logger.warning(f"Flagging {app_name} for manual review. Reasons: {reasons}")
        
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        data = []
        if os.path.exists(self.queue_file):
            try:
                with open(self.queue_file, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        # Update or append
        existing = next((item for item in data if item["app_id"] == app_id), None)
        if existing:
            existing["reasons"] = list(set(existing["reasons"] + reasons))
        else:
            data.append({
                "app_id": app_id,
                "app_name": app_name,
                "reasons": reasons,
                "status": "Pending Review"
            })
            
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2)
