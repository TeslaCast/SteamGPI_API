from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from microservices.game_data_service import crud, models
from microservices.game_data_service.database import SessionLocal, engine, get_db
import logging


models.Base.metadata.create_all(bind=engine)

router = APIRouter()

logger = logging.getLogger("microservices.game_data_service.routes")

@router.get("/doc")
async def doc():
    """
    Возвращает документацию API в формате JSON
    """
    return {
        "project": "Game Data Service",
        "description": "Микросервис для работы с данными игр и базой данных.",
        "endpoints": [
            {
                "path": "/game/{appid}",
                "method": "GET",
                "description": "Получение информации об игре в нескольких регионах",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam"
                },
                "response": "JSON-массив с информацией по каждому региону"
            },
            {
                "path": "/game",
                "method": "POST",
                "description": "Создание новой записи игры",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam",
                    "game_data": "list, обязательно - Данные игры",
                    "regions": "list, обязательно - Список регионов"
                },
                "response": "Созданная запись игры"
            },
            {
                "path": "/game/{appid}",
                "method": "PUT",
                "description": "Обновление данных игры",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam",
                    "game_data": "list, обязательно - Обновленные данные игры"
                },
                "response": "Обновленная запись игры"
            }
        ],
        "error_handling": {
            "404": "Not Found – Игра не найдена",
            "500": "Internal Server Error – Внутренняя ошибка сервера"
        }
    }

@router.get("/game/{appid}")
def get_game(appid: int, db: Session = Depends(get_db)):
    steam_regions = ["US", "RU", "TR", "KZ"]
    print(f"Хочу найти игру: {appid}")
    game = crud.get_game_by_appid_and_region(db, appid, steam_regions)

    if game == "True":
        print("Нашел игру, но не для всех регионов!")
        return JSONResponse(status_code=404, content={"error": "Game not found in some regions"})
    elif game:
        print("Игру нашел, возвращаю её")
        return game
    else:
        print("Игра не найдена")
        raise HTTPException(status_code=404, detail="Game not found")

@router.post("/game")
def create_game(appid: int = Body(...), game_data: List = Body(...), regions: List[str] = Body(...), db: Session = Depends(get_db)):
    try:
        created_games = crud.create_game(db, appid, game_data, regions)
        return created_games
    except Exception as e:
        logger.error(f"Error creating game {appid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/game/{appid}")
def update_game(appid: int, game_data: List[dict] = Body(...), db: Session = Depends(get_db)):
    try:
        print(f"Начинаю обновление данных. На входе: {game_data}")
        updated_game = crud.update_game(db, appid, game_data)
        print(f"Закончил обновление данных: на выходе {updated_game}")
        if not updated_game:
            raise HTTPException(status_code=404, detail="Game not found")
        return updated_game
    except Exception as e:
        logger.error(f"Error updating game {appid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
