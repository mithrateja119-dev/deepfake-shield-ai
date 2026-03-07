import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.database.sqlite import Base, engine

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_history_endpoint():
    response = client.get("/api/history")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "history" in response.json()

def test_invalid_file_upload():
    # Attempt to upload a .txt file which should fail validation
    files = {"file": ("test.txt", b"dummy content", "text/plain")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 400
    assert "not allowed" in response.json()["error"].lower()

def test_valid_image_upload():
    # Valid image upload simulating the front-end behaviour
    files = {"file": ("test_image.jpg", b"\xFF\xD8\xFF\xE0", "image/jpeg")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "confidence" in data
    assert data["label"] in ["fake", "real"]
    assert "heatmap_base64" in data["explanation"]
