import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: Get activities

def test_get_activities():
    # Arrange: None needed, using default in-memory DB
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test: Sign up for activity

def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Cleanup: Remove test user
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test: Prevent duplicate signup

def test_prevent_duplicate_signup():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")

# Test: Unregister participant

def test_unregister_from_activity():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

# Test: Unregister non-existent participant

def test_unregister_nonexistent():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
