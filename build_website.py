#!/usr/bin/env python3
"""Build script to assemble the static website assets."""
import os
import shutil
import json
from config.settings import settings
from utils.logger import get_logger

logger = get_logger()

def main():
    website_dir = os.path.join(os.path.dirname(__file__), "website")
    assets_data_dir = os.path.join(website_dir, "assets", "data")
    assets_charts_dir = os.path.join(website_dir, "assets", "charts")
    
    # Create directories
    os.makedirs(assets_data_dir, exist_ok=True)
    os.makedirs(assets_charts_dir, exist_ok=True)
    
    # 1. Copy JSON files
    json_files = [
        "verified_results.json",
        "analytics.json",
        "insights.json",
        "summary.json",
        "executive_report.json"
    ]
    
    for f in json_files:
        src = os.path.join(settings.OUTPUT_FOLDER, f)
        dst = os.path.join(assets_data_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            logger.info(f"Copied {f}")
        else:
            # Create empty placeholder if it doesn't exist
            with open(dst, 'w') as out_f:
                if f == "verified_results.json":
                    json.dump([], out_f)
                else:
                    json.dump({}, out_f)
            logger.warning(f"File {f} not found, created empty placeholder.")
            
    # 2. Copy Charts
    charts_src_dir = os.path.join(settings.OUTPUT_FOLDER, "charts")
    if os.path.exists(charts_src_dir):
        for f in os.listdir(charts_src_dir):
            if f.endswith(".png"):
                shutil.copy2(os.path.join(charts_src_dir, f), os.path.join(assets_charts_dir, f))
        logger.info("Copied charts.")
    else:
        logger.warning("Charts directory not found.")
        
    logger.info(f"Website assets assembled successfully in {website_dir}.")

if __name__ == "__main__":
    main()
