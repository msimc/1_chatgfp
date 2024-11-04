import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fca_categorization.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_company_data():
    return {
        "name": "Test Company",
        "firm_reference_number": "123456",
        "regulatory_status": "Authorized",
        "permissions": ["investment management", "retail clients"],
        "assets_under_management": 1000000000,
        "employee_count": 250,
        "country_operations": ["UK"]
    }
