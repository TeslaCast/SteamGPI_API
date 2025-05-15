import pytest
from fastapi.testclient import TestClient
from microservices.game_data_service.main import app
from microservices.game_data_service.database import SessionLocal, engine
from microservices.game_data_service import models

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Создаем таблицы
    models.Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после тестов
    models.Base.metadata.drop_all(bind=engine)

def test_get_game_not_found():
    response = client.get("/game/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}

def test_create_and_get_game():
    db = SessionLocal()
    game = models.Game(appid=221100, data=[{
        "appid": 221100,
        "region": "RU",
        "name": "Test Game",
        "is_free": False,
        "currency": "RUB",
        "initial_price": 1000,
        "final_price": 500,
        "discount_percent": 50,
        "release_date": "2022-01-01"
    }])
    db.add(game)
    db.commit()
    db.refresh(game)
    db.close()

    response = client.get("/game/221100")
    assert response.status_code == 404
    data = response.json()
    assert isinstance(data, dict)
    

