import pytest
from fastapi.testclient import TestClient
from APP.main import app

client = TestClient(app)

def test_read_index():
    response = client.get("/")
    assert response.status_code == 200

def test_read_privacy():
    response = client.get("/privacy")
    assert response.status_code == 200
