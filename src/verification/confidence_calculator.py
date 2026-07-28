"""Calculates confidence scores for extracted fields."""
from utils.logger import get_logger

logger = get_logger()

class ConfidenceCalculator:
    def calculate_field_confidence(self, evidence_validity: dict, is_conflicting: bool, llm_confidence: float) -> float:
        """
        Calculates confidence for a single field based on:
        - Reachability of evidence
        - Official domain status
        - LLM's own certainty
        - Presence of conflicts
        """
        score = llm_confidence
        
        # Penalties
        if not evidence_validity.get("reachable", False):
            score -= 40
            
        if not evidence_validity.get("official", False):
            score -= 20
            
        if is_conflicting:
            score -= 30
            
        return max(0.0, min(100.0, score))

    def calculate_overall_confidence(self, verified_fields: dict) -> float:
        """Averages the confidence of all verified fields."""
        scores = []
        for key, field_data in verified_fields.items():
            if isinstance(field_data, dict) and "confidence" in field_data:
                scores.append(field_data["confidence"])
            elif hasattr(field_data, "confidence"):
                scores.append(field_data.confidence)
                
        if not scores:
            return 0.0
            
        return sum(scores) / len(scores)
