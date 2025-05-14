from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging

router = APIRouter()
logger = logging.getLogger("api_gateway.routes")

GAME_DATA_SERVICE_URL = "http://localhost:8001"
STEAM_INTEGRATION_SERVICE_URL = "http://localhost:8002"

@router.get("/doc")
async def doc():
    return {
        "project": "SteamGPI API Gateway",
        "description": "API Gateway для микросервисов Steam GeoPricing Inspector.",
        "endpoints": [
            {
                "path": "/game/{appid}",
                "method": "GET",
                "description": "Получение информации об игре из микросервисов",
                "parameters": {
                    "appid": "integer, обязательно - Уникальный идентификатор игры в Steam"
                },
                "response": "JSON-объект с информацией о продукте"
            }
        ]
    }

@router.get("/game/{appid}")
async def get_game(appid: int):
    async with httpx.AsyncClient() as client:
        try:
            # Сначала запрос к Game Data Service
            response = await client.get(f"{GAME_DATA_SERVICE_URL}/game/{appid}")
            if response.status_code == 404:
                # Если нет в базе, запрос к Steam Integration Service
                steam_response = await client.get(f"{STEAM_INTEGRATION_SERVICE_URL}/game/{appid}")
                if steam_response.status_code == 200:
                    # Возвращаем JSON как есть, без попытки сериализации в объект
                    return JSONResponse(content=steam_response.json())
                else:
                    raise HTTPException(status_code=steam_response.status_code, detail="Game not found")
            elif response.status_code == 200:
                return JSONResponse(content=response.json())
            else:
                raise HTTPException(status_code=response.status_code, detail="Error fetching game data")
        except Exception as e:
            logger.error(f"Error in API Gateway fetching game {appid}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
