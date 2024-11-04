import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "version" in response.json()
    assert "endpoints" in response.json()

def test_categorize_endpoint_valid_data():
    data = {
        "name": "Test Company",
        "firm_reference_number": "123456",
        "regulatory_status": "Authorized",
        "permissions": ["investment management", "retail clients"],
        "assets_under_management": 1000000000,
        "employee_count": 250
    }
    
    response = client.post("/categorize", json=data)
    assert response.status_code == 200
    
    result = response.json()
    assert "smcr_category" in result
    assert "regulatory_status" in result
    assert "business_activities" in result
    assert "risk_score" in result
    assert isinstance(result["risk_score"], float)
    assert 0 <= result["risk_score"] <= 100

def test_categorize_endpoint_invalid_frn():
    data = {
        "name": "Test Company",
        "firm_reference_number": "12345",  # Invalid - too short
        "regulatory_status": "Authorized"
    }
    
    response = client.post("/categorize", json=data)
    assert response.status_code == 422  # FastAPI returns 422 for validation errors

def test_categorize_endpoint_minimal_data():
    data = {
        "name": "Minimal Company"
    }
    
    response = client.post("/categorize", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["regulatory_status"] == "Unknown"

def test_categorize_endpoint_complex_permissions():
    data = {
        "name": "Complex Company",
        "permissions": [
            "investment management",
            "retail clients",
            "professional clients",
            "insurance mediation",
            "mortgage advice",
            "banking services"
        ],
        "assets_under_management": 5000000000,
        "employee_count": 1000,
        "country_operations": ["UK", "US", "EU"]
    }
    
    response = client.post("/categorize", json=data)
    assert response.status_code == 200
    result = response.json()
    
    assert "Investment Management" in result["business_activities"]
    assert result["geographic_reach"] == "International"
    assert len(result["regulatory_implications"]) > 0
