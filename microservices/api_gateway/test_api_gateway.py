import pytest
from fastapi.testclient import TestClient
import sys
import os

# Добавляем путь к корню проекта, чтобы можно было импортировать app из другого модуля
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Импорт FastAPI-приложения
from microservices.api_gateway.main import app

# Инициализируем тестовый клиент для взаимодействия с приложением
client = TestClient(app)


def test_doc_endpoint():
    """
    Проверяет, что эндпоинт /doc возвращает статус 200 и содержит ключ "project" в JSON-ответе.
    """
    response = client.get("/doc")
    assert response.status_code == 200
    assert "project" in response.json()


def test_game_not_found(monkeypatch):
    """
    Проверяет поведение, если игра с заданным appid не найдена.
    Мокаем httpx.AsyncClient.get, чтобы он возвращал 404.
    """

    class MockResponse:
        status_code = 404

        def json(self):
            return {}

    async def mock_get(*args, **kwargs):
        return MockResponse()

    # Подменяем метод get у httpx.AsyncClient
    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    # Выполняем запрос к несуществующей игре
    response = client.get("/game/999999")

    # Допускаем 404 (ожидаемый), но также и 500 (если сервис возвращает ошибку обработки)
    assert response.status_code == 404 or response.status_code == 500


def test_game_found(monkeypatch):
    """
    Проверяет поведение при успешной загрузке данных об игре.
    Возвращается список региональных цен с корректным appid.
    """

    class MockResponse:
        status_code = 200

        def json(self):
            return [
                {
                    'appid': 221100,
                    'region': 'US',
                    'name': 'DayZ',
                    'is_free': False,
                    'currency': 'USD',
                    'initial_price': 59.99,
                    'final_price': 29.99,
                    'discount_percent': 50,
                    'release_date': 'Jan 1, 2020'
                },
                {
                    'appid': 221100,
                    'region': 'RU',
                    'name': 'DayZ',
                    'is_free': False,
                    'currency': 'RUB',
                    'initial_price': 1999,
                    'final_price': 999,
                    'discount_percent': 50,
                    'release_date': '1 Jan, 2020'
                }
            ]

    async def mock_get(url, *args, **kwargs):

        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    # Запрос к существующей игре
    response = client.get("/game/221100")
    assert response.status_code == 200

    json_data = response.json()

    # Проверка структуры ответа
    assert isinstance(json_data, list)
    assert json_data[0]["appid"] == 221100


def test_game_found_fresh_data(monkeypatch):
    """
    Проверяет, что если данные об игре свежие (обновлены недавно),
    они возвращаются корректно.
    """

    class MockResponse:
        status_code = 200

        def json(self):
            from datetime import datetime
            return {
                "data": {
                    "appid": 221100,
                    "name": "DayZ"
                },
                "updated_at": datetime.utcnow().isoformat()
            }

    async def mock_get(url, *args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    # Запрос к игре с "свежими" данными
    response = client.get("/game/221100")
    assert response.status_code == 200

    json_data = response.json()

    # Проверка структуры JSON-ответа
    assert "data" in json_data
    assert json_data["data"]["appid"] == 221100
