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

def test_get_info_invalid_appid_letters():
    response = client.get("/game/ijrgawer")
    assert response.status_code == 422

def test_response_data_fields():
    response = client.get("/game/221100")
    assert response.status_code == 200
    data = response.json()
    sample = data[0]
    expected_keys = {"appid", "region", "name", "is_free", "currency", "initial_price", "final_price", "discount_percent", "release_date"}
    assert expected_keys.issubset(sample.keys())

def test_nonexistent_appid_returns_break():
    response = client.get("/game/999999999")  # маловероятный appid
    assert response.status_code == 200
    data = response.json()
    assert all(item.get("break") for item in data)
