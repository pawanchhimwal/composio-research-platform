"""Discovers statistical correlations and patterns across the dataset."""
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

class PatternDiscovery:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def discover_patterns(self) -> dict:
        """Finds statistically significant relationships using crosstabs."""
        if self.df.empty:
            return {}

        patterns = {}
        
        # Pattern 1: Category vs Authentication
        cat_auth = pd.crosstab(self.df['category'], self.df['auth_primary'], normalize='index')
        patterns["category_auth"] = self._extract_dominant_patterns(cat_auth)
        
        # Pattern 2: Buildability vs Self Service
        build_ss = pd.crosstab(self.df['buildability'], self.df['self_serve'], normalize='index')
        patterns["buildability_self_serve"] = self._extract_dominant_patterns(build_ss)
        
        # Pattern 3: Category vs MCP Support
        cat_mcp = pd.crosstab(self.df['category'], self.df['mcp_support'], normalize='index')
        patterns["category_mcp"] = self._extract_dominant_patterns(cat_mcp)
        
        # Pattern 4: Category vs Blockers
        cat_blocker = pd.crosstab(self.df['category'], self.df['blocker'], normalize='index')
        patterns["category_blockers"] = self._extract_dominant_patterns(cat_blocker)
        
        logger.info("Patterns discovered.")
        return patterns

    def _extract_dominant_patterns(self, cross_tab: pd.DataFrame, threshold: float = 0.5) -> list:
        """Helper to find relationships occurring >50% of the time in a cohort."""
        findings = []
        for index, row in cross_tab.iterrows():
            for col, value in row.items():
                if value >= threshold:
                    findings.append({
                        "cohort": str(index),
                        "dominant_trait": str(col),
                        "percentage": round(value * 100, 1)
                    })
        return findings
