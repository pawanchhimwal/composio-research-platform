"""Calculates integration priority scores for applications."""
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

class PriorityScorer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def rank_applications(self) -> dict:
        """Assigns a score to each app and ranks them."""
        if self.df.empty:
            return {}
            
        def calculate_score(row):
            score = 0
            # Buildability points
            if row['buildability'] == "Ready Today": score += 35
            elif row['buildability'] == "Easy": score += 30
            elif row['buildability'] == "Medium": score += 15
            
            # Auth points
            if row['auth_primary'] == "OAuth2": score += 20
            elif row['auth_primary'] == "API Key": score += 15
            
            # API points
            if row['api_type'] in ["REST", "GraphQL"]: score += 20
            
            # Access points
            if row['self_serve'] in ["Free/Trial", "Paid Plan"]: score += 15
            
            # Confidence points (scaled)
            score += (row['overall_confidence'] / 100.0) * 10
            
            return min(100.0, score)
            
        # Calculate
        scored_df = self.df.copy()
        scored_df['priority_score'] = scored_df.apply(calculate_score, axis=1)
        
        # Sort and categorize
        scored_df = scored_df.sort_values(by='priority_score', ascending=False)
        
        top_priority = scored_df.head(20)[['name', 'priority_score', 'buildability', 'auth_primary']].to_dict('records')
        lowest_priority = scored_df.tail(20)[['name', 'priority_score', 'blocker']].to_dict('records')
        
        return {
            "top_priority": top_priority,
            "lowest_priority": lowest_priority
        }
