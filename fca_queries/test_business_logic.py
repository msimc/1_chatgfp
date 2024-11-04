import os
import sys
import pytest

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fca_categorization.main import (
    analyze_permissions,
    calculate_risk_metrics,
    determine_regulatory_implications,
    FCACompanyInfo,
    ClientType,
    SizeComplexity,
    RiskProfile
)

def test_analyze_permissions():
    permissions = [
        "investment management",
        "retail clients",
        "insurance mediation",
        "mortgage advice"
    ]
    activities, specializations = analyze_permissions(permissions)
    
    assert "Investment Management" in activities
    assert "Insurance Services" in activities
    assert "Mortgage Services" in activities
    assert isinstance(activities, list)
    assert isinstance(specializations, list)

def test_analyze_permissions_empty():
    activities, specializations = analyze_permissions([])
    assert activities == []
    assert specializations == []

def test_calculate_risk_metrics():
    company_info = FCACompanyInfo(
        name="Test Company",
        permissions=["investment management", "retail clients"],
        assets_under_management=1000000000
    )
    
    risk_score, risk_profile = calculate_risk_metrics(
        company_info,
        SizeComplexity.LARGE,
        ["Investment Management"],
        [ClientType.RETAIL]
    )
    
    assert isinstance(risk_score, float)
    assert 0 <= risk_score <= 100
    assert isinstance(risk_profile, RiskProfile)

def test_risk_metrics_high_risk():
    company_info = FCACompanyInfo(
        name="High Risk Company",
        permissions=["investment management", "retail clients", "banking services"],
        assets_under_management=5000000000
    )
    
    risk_score, risk_profile = calculate_risk_metrics(
        company_info,
        SizeComplexity.LARGE,
        ["Investment Management", "Banking Services"],
        [ClientType.RETAIL, ClientType.PROFESSIONAL]
    )
    
    assert risk_score >= 70
    assert risk_profile == RiskProfile.HIGH

def test_determine_regulatory_implications():
    categorization = {
        "size_and_complexity": SizeComplexity.LARGE,
        "client_base": [ClientType.RETAIL],
        "risk_profile": RiskProfile.HIGH
    }
    
    implications = determine_regulatory_implications(categorization)
    
    assert isinstance(implications, list)
    assert any("Consumer Duty" in imp for imp in implications)
    assert any("Enhanced" in imp for imp in implications)
    assert any("risk management" in imp.lower() for imp in implications)
