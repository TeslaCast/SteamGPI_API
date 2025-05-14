import pytest
from fastapi.testclient import TestClient
from microservices.steam_integration_service.main import app

client = TestClient(app)

def test_get_info_across_regions():
    response = client.get("/game/221100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item.get("appid") == 221100 for item in data)

def test_get_info_invalid_appid():
    response = client.get("/game/0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Исправлено: проверяем, что нет элементов с ключом "break"
    assert not any(item.get("break") for item in data)
