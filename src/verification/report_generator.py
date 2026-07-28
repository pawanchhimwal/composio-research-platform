"""Generates the final accuracy and verification report."""
import json
import os

class ReportGenerator:
    def __init__(self, report_file: str):
        self.report_file = report_file
        self.stats = {
            "apps_processed": 0,
            "verified_automatically": 0,
            "flagged_for_review": 0,
            "total_mismatches": 0,
            "average_confidence": 0.0
        }
        self.confidence_sum = 0.0

    def update_stats(self, is_flagged: bool, mismatches_count: int, confidence: float):
        """Updates internal statistics running totals."""
        self.stats["apps_processed"] += 1
        
        if is_flagged:
            self.stats["flagged_for_review"] += 1
        else:
            self.stats["verified_automatically"] += 1
            
        self.stats["total_mismatches"] += mismatches_count
        self.confidence_sum += confidence
        
        if self.stats["apps_processed"] > 0:
            self.stats["average_confidence"] = self.confidence_sum / self.stats["apps_processed"]

    def save_report(self):
        """Saves the final report to disk."""
        os.makedirs(os.path.dirname(self.report_file), exist_ok=True)
        with open(self.report_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
