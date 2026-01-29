import pytest
from fastapi.testclient import TestClient
from src.app import app

 
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert isinstance(data["Soccer Team"], dict)

def test_signup_and_unregister(client):
    test_email = "testuser@mergington.edu"
    activity = "Soccer Team"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200 or (
        response.status_code == 400 and "already signed up" in response.text
    )
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", json={"email": test_email})
    assert response.status_code == 200 or (
        response.status_code == 400 and "Participant not found" in response.text
    )
