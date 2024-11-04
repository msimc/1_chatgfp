import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
from src.fca_categorization.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    fake_users_db
)
from src.fca_categorization.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_protected_route_without_token():
    response = client.post(
        "/categorize",
        json={
            "name": "Test Company",
            "firm_reference_number": "123456"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_with_token():
    # First get token
    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    
    # Use token to access protected route
    response = client.post(
        "/categorize",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Company",
            "firm_reference_number": "123456"
        }
    )
    assert response.status_code == 200

def test_get_current_user():
    # First get token
    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user info
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_token_creation():
    token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(minutes=30)
    )
    assert isinstance(token, str)
    assert len(token) > 0
