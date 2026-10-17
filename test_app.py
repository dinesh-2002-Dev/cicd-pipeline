import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cloud & IAM Service Portal" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_iam_unauthorized_blocked(client):
    response = client.get("/api/secure-data")
    assert response.status_code == 401

def test_iam_authorized_allowed(client):
    response = client.get("/api/secure-data", headers={"Authorization": "Bearer admin-secret-123"})
    assert response.status_code == 200
    assert response.get_json()["role"] == "IAM-Admin"
