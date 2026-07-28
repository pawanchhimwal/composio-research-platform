import pandas as pd
import pytest
import os
import sys

# Ensure config module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.schema import ApplicationIntelligence
from config.constants import AuthMethod, ApiType, Buildability, VerificationState, SelfServeStatus

def test_apps_master_csv_exists_and_valid():
    """Verify the CSV exists, has 100 rows, and no duplicate IDs."""
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'apps_master.csv')
    assert os.path.exists(csv_path), "Master CSV file is missing."
    
    df = pd.read_csv(csv_path)
    
    assert len(df) == 100, f"Expected 100 apps, found {len(df)}"
    
    # Check for required columns
    expected_cols = ["id", "name", "category", "website"]
    for col in expected_cols:
        assert col in df.columns, f"Missing required column: {col}"
        
    # Check no duplicate IDs
    assert df["id"].is_unique, "Duplicate IDs found in master CSV"
    
    # Check no missing names or websites
    assert not df["name"].isnull().any(), "Some apps are missing a name"
    assert not df["website"].isnull().any(), "Some apps are missing a website"


def test_schema_validation_passes():
    """Verify that a well-formed JSON object passes Pydantic validation."""
    valid_data = {
        "id": 1,
        "name": "Salesforce",
        "category": "CRM and Sales",
        "website": "https://salesforce.com",
        "description": "Leading CRM",
        "authentication": [AuthMethod.OAUTH2, AuthMethod.API_KEY],
        "self_serve": SelfServeStatus.PAID_PLAN,
        "developer_access": "Requires dev account",
        "api_type": ApiType.REST,
        "api_surface": "Extensive",
        "api_breadth": "Broad",
        "mcp_support": False,
        "buildability": Buildability.READY,
        "evidence": {
            "authentication": {
                "url": "https://developer.salesforce.com/docs/auth",
                "reason": "OAuth2 is listed as primary."
            }
        },
        "confidence": 95.0,
        "verification_status": VerificationState.PENDING
    }
    
    app = ApplicationIntelligence(**valid_data)
    assert app.id == 1
    assert app.name == "Salesforce"
    assert app.confidence == 95.0

def test_schema_validation_fails_on_invalid_data():
    """Verify that an invalid confidence score or enum fails validation."""
    from pydantic import ValidationError
    
    invalid_data = {
        "id": 2,
        "name": "HubSpot",
        "category": "CRM",
        "website": "https://hubspot.com",
        "description": "",
        "authentication": ["Invalid Auth Type"], # Invalid Enum
        "self_serve": SelfServeStatus.FREE_TRIAL,
        "api_type": ApiType.REST,
        "buildability": Buildability.EASY,
        "confidence": 150.0, # Invalid (should be <= 100.0)
        "evidence": {},
        "verification_status": VerificationState.PENDING
    }
    
    with pytest.raises(ValidationError):
        ApplicationIntelligence(**invalid_data)
