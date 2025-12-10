import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test signup for activity
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu")
])
def test_signup_for_activity(activity, email):
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Second signup should fail (already registered)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# Test remove participant
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu")
])
def test_remove_participant(activity, email):
    # Remove should succeed
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    # Remove again should fail
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# Test signup for non-existent activity
def test_signup_nonexistent_activity():
    response = client.post("/activities/NonExistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Test remove from non-existent activity
def test_remove_nonexistent_activity():
    response = client.delete("/activities/NonExistent/participants/anyone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
