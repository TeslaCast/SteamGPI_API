import pytest
from fastapi.testclient import TestClient
from microservices.api_gateway.main import app

client = TestClient(app)

def test_doc_endpoint():
    response = client.get("/doc")
    assert response.status_code == 200
    assert "project" in response.json()

def test_game_not_found(monkeypatch):
    class MockResponse:
        status_code = 404
        def json(self):
            return {}

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    response = client.get("/game/999999")
    assert response.status_code == 404 or response.status_code == 500

def test_game_found(monkeypatch):
    class MockResponse:
        status_code = 200
        def json(self):
            return {"appid": 221100, "name": "DayZ"}

    async def mock_get(url, *args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    response = client.get("/game/221100")
    assert response.status_code == 200
    assert response.json()["appid"] == 221100
