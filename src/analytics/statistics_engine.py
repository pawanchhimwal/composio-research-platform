"""Computes statistical distributions across the dataset."""
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

class StatisticsEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def compute_all(self) -> dict:
        """Computes all major statistics and returns a dictionary."""
        if self.df.empty:
            return {}
            
        stats = {
            "total_apps": len(self.df),
            "average_confidence": self.df["overall_confidence"].mean(),
            "authentication_distribution": self.df["auth_primary"].value_counts().to_dict(),
            "category_distribution": self.df["category"].value_counts().to_dict(),
            "api_type_distribution": self.df["api_type"].value_counts().to_dict(),
            "self_serve_distribution": self.df["self_serve"].value_counts().to_dict(),
            "buildability_distribution": self.df["buildability"].value_counts().to_dict(),
            "mcp_support_distribution": self.df["mcp_support"].value_counts().to_dict(),
            "blockers_distribution": self.df["blocker"].value_counts().to_dict()
        }
        
        logger.info("Statistics generated successfully.")
        return stats
