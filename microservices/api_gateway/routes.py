from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging

router = APIRouter()
logger = logging.getLogger("api_gateway.routes")

GAME_DATA_SERVICE_URL = "http://localhost:8001"
STEAM_INTEGRATION_SERVICE_URL = "http://localhost:8002"


@router.get("/game/{appid}")
async def get_game(appid: int):
    async with httpx.AsyncClient() as client:
        try:
            # Сначала запрос к Game Data Service
            print("Пробую запрос к бд")
            response = await client.get(f"{GAME_DATA_SERVICE_URL}/game/{appid}")
            print(f"Получил: {response} response status_code = {response.status_code}")
            if response.status_code == 404:
                print("Не нашел игру в бд")
                # Если нет в базе, запрос к Steam Integration Service
                print("Пробую запрос к парсеру")
                steam_response = await client.get(f"{STEAM_INTEGRATION_SERVICE_URL}/game/{appid}")
                print(f"Получил: {steam_response}\nresponse status_code = {steam_response.status_code}")
                if steam_response.status_code == 200:
                    # Возвращаем JSON как есть, без попытки сериализации в объект
                    print(f"Вот что получает пользователь: {steam_response.json()}")
                    return JSONResponse(content=steam_response.json())
                else:
                    print("Парсер ничего не вернул")
                    raise HTTPException(status_code=steam_response.status_code, detail="Game not found")
            elif response.status_code == 200:
                print(f"В бд есть такая запись, выдаю пользователю: {response.json()}")
                return JSONResponse(content=response.json())
            else:
                print("Миша, все сломалось!")
                raise HTTPException(status_code=response.status_code, detail="Error fetching game data")
        except Exception as e:
            logger.error(f"Error in API Gateway fetching game {appid}: {e}")
            print(f"Блядь, все все сломалось!!! {e}")
            raise HTTPException(status_code=500, detail=str(e))
