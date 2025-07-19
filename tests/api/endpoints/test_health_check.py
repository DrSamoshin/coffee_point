from fastapi.testclient import TestClient

from app.main import main_app

client = TestClient(main_app)


def test_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "application is running"}
