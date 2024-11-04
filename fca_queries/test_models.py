import os
import sys
from datetime import date
import pytest
from pydantic import ValidationError

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fca_categorization.main import FCACompanyInfo, FCACategorization

def test_valid_fca_company_info():
    company = FCACompanyInfo(
        name="Test Company",
        firm_reference_number="123456",
        regulatory_status="Authorized",
        permissions=["investment management"],
        assets_under_management=1000000,
        employee_count=100
    )
    assert company.name == "Test Company"
    assert company.firm_reference_number == "123456"

def test_invalid_firm_reference_number():
    with pytest.raises(ValidationError):
        FCACompanyInfo(
            name="Test Company",
            firm_reference_number="12345"  # Too short
        )
    
    with pytest.raises(ValidationError):
        FCACompanyInfo(
            name="Test Company",
            firm_reference_number="1234567"  # Too long
        )

    with pytest.raises(ValidationError):
        FCACompanyInfo(
            name="Test Company",
            firm_reference_number="12345A"  # Contains letter
        )

def test_optional_fields():
    company = FCACompanyInfo(name="Test Company")
    assert company.firm_reference_number is None
    assert company.permissions == []
    assert company.assets_under_management is None

def test_date_authorized_validation():
    company = FCACompanyInfo(
        name="Test Company",
        date_authorized=date(2023, 1, 1)
    )
    assert company.date_authorized == date(2023, 1, 1)
