#!/usr/bin/env python3
"""Entry point for the Composio Verification & QA Agent pipeline."""
import os
import sys
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import settings
from src.tools.search import WebSearcher
from src.tools.scraper import DocScraper
from src.verification.verifier_agent import VerifierAgent
from src.verification.evidence_validator import EvidenceValidator
from src.verification.difference_detector import DifferenceDetector
from src.verification.confidence_calculator import ConfidenceCalculator
from src.verification.manual_review_queue import ManualReviewQueue
from src.verification.report_generator import ReportGenerator
from utils.logger import get_logger

logger = get_logger()

def main():
    input_file = os.path.join(settings.OUTPUT_FOLDER, "results.json")
    verified_file = os.path.join(settings.OUTPUT_FOLDER, "verified_results.json")
    report_file = os.path.join(settings.OUTPUT_FOLDER, "verification_report.json")
    mismatches_file = os.path.join(settings.OUTPUT_FOLDER, "mismatches.json")
    queue_file = os.path.join(settings.OUTPUT_FOLDER, "manual_review_queue.json")
    
    if not os.path.exists(input_file):
        logger.error(f"Cannot run verification: {input_file} not found.")
        return

    try:
        with open(input_file, 'r') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError:
        logger.error("Failed to parse results.json")
        return
        
    searcher = WebSearcher()
    scraper = DocScraper()
    agent = VerifierAgent()
    evidence_validator = EvidenceValidator()
    diff_detector = DifferenceDetector(mismatches_file)
    conf_calc = ConfidenceCalculator()
    review_queue = ManualReviewQueue(queue_file)
    report_gen = ReportGenerator(report_file)
    
    verified_results = []
    
    logger.info("Starting Verification Pipeline...")
    
    for app in raw_data:
        app_id = app.get("id")
        app_name = app.get("name")
        app_website = app.get("website")
        
        logger.info(f"Verifying {app_name}...")
        
        # 1. Validate Evidence URLs from Phase 3
        evidence_validity = {}
        original_evidence = app.get("evidence", {})
        if isinstance(original_evidence, dict):
            for field, ev_obj in original_evidence.items():
                if ev_obj and isinstance(ev_obj, dict) and "url" in ev_obj:
                    url = ev_obj["url"]
                    evidence_validity[field] = evidence_validator.validate_evidence(url, app_website)
                    
        # 2. Re-Scrape to avoid trusting old markdown completely
        urls = searcher.search_docs(app_name)
        context = scraper.scrape_multiple(urls) if urls else ""
        
        # 3. Independent LLM Extraction
        verified_raw = agent.verify_app(app, context)
        
        if not verified_raw:
            logger.error(f"Verification failed for {app_name}")
            review_queue.flag_for_review(app_id, app_name, ["LLM Verification Failed"])
            continue
            
        verified_raw["id"] = app_id
        verified_raw["name"] = app_name
        
        # 4. Difference Detection
        mismatches = diff_detector.detect_differences(app_id, app_name, app, verified_raw)
        
        # 5. Confidence Calculation & Flagging
        is_flagged = False
        reasons = []
        
        overall_conf = verified_raw.get("overall_confidence", 0.0)
        if overall_conf < settings.CONFIDENCE_THRESHOLD * 100:
            is_flagged = True
            reasons.append(f"Low Overall Confidence: {overall_conf}")
            
        if mismatches:
            is_flagged = True
            reasons.append(f"Found {len(mismatches)} Mismatches")
            
        if is_flagged:
            review_queue.flag_for_review(app_id, app_name, reasons)
            verified_raw["verification_status"] = "Requires_Human"
        else:
            verified_raw["verification_status"] = "Agent_Verified"
            
        report_gen.update_stats(is_flagged, len(mismatches), overall_conf)
        verified_results.append(verified_raw)
        
    # Save Verified Results
    with open(verified_file, 'w') as f:
        json.dump(verified_results, f, indent=2)
        
    # Save Report
    report_gen.save_report()
    
    logger.info("Verification Pipeline Finished.")

if __name__ == "__main__":
    main()
