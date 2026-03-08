import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_verify_face_endpoint_missing_files():
    response = client.post("/verify-face")
    assert response.status_code == 422 # FastAPI built-in validation for missing form-data

def test_verify_face_invalid_format():
    files = {
        'reference_image': ('ref.txt', b'fake data', 'text/plain'),
        'test_image': ('test.txt', b'fake data', 'text/plain')
    }
    response = client.post("/verify-face", files=files)
    assert response.status_code == 400
    assert response.json()["success"] is False
    assert "Only JPG and PNG supported" in response.json()["error"]
