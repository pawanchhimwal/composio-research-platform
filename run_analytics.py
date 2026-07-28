#!/usr/bin/env python3
"""Entry point for the Composio Analytics & Pattern Discovery Engine."""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import settings
from src.analytics.aggregator import Aggregator
from src.analytics.statistics_engine import StatisticsEngine
from src.analytics.pattern_discovery import PatternDiscovery
from src.analytics.priority_scorer import PriorityScorer
from src.analytics.insight_generator import InsightGenerator
from src.analytics.chart_generator import ChartGenerator
from utils.logger import get_logger

logger = get_logger()

def main():
    verified_file = os.path.join(settings.OUTPUT_FOLDER, "verified_results.json")
    
    analytics_file = os.path.join(settings.OUTPUT_FOLDER, "analytics.json")
    insights_file = os.path.join(settings.OUTPUT_FOLDER, "insights.json")
    summary_file = os.path.join(settings.OUTPUT_FOLDER, "summary.json")
    exec_report_file = os.path.join(settings.OUTPUT_FOLDER, "executive_report.json")
    charts_dir = os.path.join(settings.OUTPUT_FOLDER, "charts")
    
    logger.info("Starting Analytics Engine...")
    
    # 1. Aggregate
    aggregator = Aggregator(verified_file)
    df = aggregator.load_dataframe()
    
    if df.empty:
        logger.error("No verified data to analyze. Exiting.")
        return
        
    # 2. Statistics
    stats_engine = StatisticsEngine(df)
    stats = stats_engine.compute_all()
    
    with open(analytics_file, 'w') as f:
        json.dump(stats, f, indent=2)
        
    # 3. Pattern Discovery
    pattern_engine = PatternDiscovery(df)
    patterns = pattern_engine.discover_patterns()
    
    with open(insights_file, 'w') as f:
        json.dump(patterns, f, indent=2)
        
    # 4. Priority Scoring
    scorer = PriorityScorer(df)
    rankings = scorer.rank_applications()
    
    with open(summary_file, 'w') as f:
        json.dump(rankings, f, indent=2)
        
    # 5. Insight Generation (Executive Report)
    insight_gen = InsightGenerator()
    executive_findings = insight_gen.generate_executive_report(stats, patterns, rankings)
    
    with open(exec_report_file, 'w') as f:
        json.dump(executive_findings, f, indent=2)
        
    # 6. Chart Generation
    chart_gen = ChartGenerator(df, charts_dir)
    chart_gen.generate_all()
    
    logger.info("Analytics Pipeline Finished Successfully.")

if __name__ == "__main__":
    main()
