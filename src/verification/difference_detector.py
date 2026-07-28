"""Compares original research outputs against verified outputs."""
import json
import os
from utils.logger import get_logger

logger = get_logger()

class DifferenceDetector:
    def __init__(self, mismatches_file: str):
        self.mismatches_file = mismatches_file

    def detect_differences(self, app_id: int, app_name: str, original: dict, verified: dict):
        """Detects mismatches between the original research and the verified result."""
        mismatches = []
        
        # Fields to compare
        fields = [
            "category", "description", "authentication", "self_serve", 
            "developer_access", "api_type", "api_breadth", 
            "mcp_support", "buildability", "blocker"
        ]
        
        for field in fields:
            orig_val = original.get(field)
            
            # Verified fields are nested under {"value": ..., "confidence": ...}
            ver_obj = verified.get(field, {})
            ver_val = ver_obj.get("value") if isinstance(ver_obj, dict) else getattr(ver_obj, "value", None)
            
            if orig_val != ver_val:
                mismatches.append({
                    "app_id": app_id,
                    "app_name": app_name,
                    "field": field,
                    "research": str(orig_val),
                    "verification": str(ver_val),
                    "status": "Mismatch"
                })
                
        if mismatches:
            self._save_mismatches(mismatches)
            
        return mismatches

    def _save_mismatches(self, new_mismatches: list):
        """Appends new mismatches to the json ledger."""
        os.makedirs(os.path.dirname(self.mismatches_file), exist_ok=True)
        data = []
        if os.path.exists(self.mismatches_file):
            try:
                with open(self.mismatches_file, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                pass
                
        data.extend(new_mismatches)
        
        with open(self.mismatches_file, 'w') as f:
            json.dump(data, f, indent=2)
