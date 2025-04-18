from main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import status

@pytest.fixture(name="client")
def client_fixture():
    """
    Create a test client for the FastAPI app."""
    client = TestClient(app)
    yield client

def test_get_info(client: TestClient):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers['content-type'] == 'application/json'
    response_json = response.json()
    assert response_json != None
    assert response_json['message'] == 'Welcome to the FastAPI application!'

