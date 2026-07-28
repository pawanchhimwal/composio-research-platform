"""Aggregates the nested verified JSON dataset into a flat Pandas DataFrame."""
import json
import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

class Aggregator:
    def __init__(self, data_file: str):
        self.data_file = data_file

    def load_dataframe(self) -> pd.DataFrame:
        """Loads and flattens verified results into a DataFrame."""
        if not os.path.exists(self.data_file):
            logger.error(f"Cannot load data. File not found: {self.data_file}")
            return pd.DataFrame()
            
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            logger.error("Failed to parse verified results JSON.")
            return pd.DataFrame()
            
        flat_records = []
        for app in data:
            record = {
                "id": app.get("id"),
                "name": app.get("name"),
                "category": self._extract_val(app.get("category")),
                "authentication": self._extract_val(app.get("authentication")),
                "self_serve": self._extract_val(app.get("self_serve")),
                "api_type": self._extract_val(app.get("api_type")),
                "mcp_support": self._extract_val(app.get("mcp_support")),
                "buildability": self._extract_val(app.get("buildability")),
                "blocker": self._extract_val(app.get("blocker")),
                "overall_confidence": app.get("overall_confidence", 0)
            }
            # Flatten lists like authentication to strings for easier groupby if needed
            if isinstance(record["authentication"], list):
                record["auth_primary"] = record["authentication"][0] if record["authentication"] else "Unknown"
            else:
                record["auth_primary"] = str(record["authentication"])
                
            flat_records.append(record)
            
        return pd.DataFrame(flat_records)

    def _extract_val(self, field: dict):
        """Extracts the value from a VerifiedField structure or returns it if flat."""
        if isinstance(field, dict) and "value" in field:
            return field["value"]
        return field
