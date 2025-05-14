from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from app import crud, models
from app.database import get_db
from app.steam import get_info_across_regions  
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/doc")
async def doc():
    """
    Возвращает документацию API в формате JSON
    """
    return {
        "project": "SteamGPI API",
        "description": "Сервис для мониторинга цен и доступности игр в Steam по регионам.",
        "base_url": "https://store.steampowered.com/api/appdetails",
        "endpoints": [
            {
                "path": "/game/{appid}",
                "method": "GET",
                "description": "Получение информации об игре в одном регионе",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam",
                    "region": "string, опционально - Код региона (например, ru, us, tr)",
                    "language": "string, опционально - Язык описания игры (например, en, ru)"
                },
                "response": "JSON-объект с информацией о продукте"
            },
            {
                "path": "/game/{appid}/regions",
                "method": "GET",
                "description": "Получение информации об игре в нескольких регионах",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam",
                    "regions": "массив строк, обязательно - Список кодов регионов (например, ru,us,eu,tr)"
                },
                "response": "JSON-массив с информацией по каждому региону"
            }
        ],
        "error_handling": {
            "400": "Bad Request – Неверный запрос (например, отсутствует appid)",
            "404": "Not Found – Игра не найдена",
            "500": "Internal Server Error – Внутренняя ошибка сервера"
        },
        "rate_limits": "API ограничено 60 запросами в минуту на один IP-адрес"
    }

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("app.routes")

@router.get("/game/{appid}")
async def get_game(appid: int, db: Session = Depends(get_db)):
    steam_regions = ["US", "RU", "TR", "KZ"]
    db_game = crud.get_game_by_appid_and_region(db, appid, steam_regions)

    if db_game == "True":
        try:
            game_data = get_info_across_regions(appid=appid, regions=steam_regions)
            if any(item.get("break") for item in game_data):
                logger.warning(f"Game not found for appid {appid} in some regions")
                return JSONResponse(status_code=404, content={"error": "Game not found"})
            crud.update_game(db, appid, game_data)
            return game_data
        except Exception as e:
            logger.error(f"Error updating game {appid}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    elif db_game:
        if db_game.updated_at < datetime.utcnow() - timedelta(minutes=1):
            try:
                game_data = get_info_across_regions(appid=appid, regions=steam_regions)
                if any(item.get("break") for item in game_data):
                    logger.warning(f"Game not found for appid {appid} in some regions")
                    return JSONResponse(status_code=404, content={"error": "Game not found"})
                crud.update_game(db, appid, game_data)
                return game_data
            except Exception as e:
                logger.error(f"Error updating game {appid}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        return db_game.data
    else:
        try:
            game_data = get_info_across_regions(appid=appid, regions=steam_regions)
            if any(item.get("break") for item in game_data):
                logger.warning(f"Game not found for appid {appid} in some regions")
                return JSONResponse(status_code=404, content={"error": "Game not found"})
            crud.create_game(db, appid, game_data, steam_regions)
            return game_data
        except Exception as e:
            logger.error(f"Error creating game {appid}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
