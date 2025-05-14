from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
import logging
from datetime import datetime, timedelta

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
            print("Пробую запрос к бд")
            response = await client.get(f"{GAME_DATA_SERVICE_URL}/game/{appid}")
            print(type(response))
            print(f"Получил: {response} response status_code = {response.status_code}")
            if response.status_code == 404:
                print("Не нашел игру в бд")
                print("Пробую запрос к парсеру")
                steam_response = await client.get(f"{STEAM_INTEGRATION_SERVICE_URL}/game/{appid}")
                print(f"Получил: {steam_response}\nresponse status_code = {steam_response.status_code}")
                if steam_response.status_code == 200:
                    steam_data = steam_response.json()
                    print(f"Вот что получает пользователь: {steam_data}")
                    create_response = await client.post(f"{GAME_DATA_SERVICE_URL}/game", json={
                        "appid": appid,
                        "game_data": steam_data,
                        "regions": [item.get("region") for item in steam_data if "region" in item]
                    })
                    if create_response.status_code not in (200, 201):
                        logger.error(f"Failed to create game data for appid {appid} in Game Data Service")
                    return JSONResponse(content=steam_data)
                else:
                    print("Парсер ничего не вернул")
                    raise HTTPException(status_code=steam_response.status_code, detail="Game not found")
            elif response.status_code == 200:
                print(f"В бд есть такая запись, выдаю пользователю: {response.json()}")
                game_data = response.json()
                updated_at_str = game_data['updated_at']
                print(f"Последнее обновление было: updated_at_str")
                if updated_at_str:
                    updated_at = datetime.fromisoformat(updated_at_str)
                    if datetime.utcnow() - updated_at > timedelta(minutes=1):
                        print("Данные устарели, обновляю: ",datetime.utcnow() - updated_at)
                        steam_response = await client.get(f"{STEAM_INTEGRATION_SERVICE_URL}/game/{appid}")
                        print(f"Получаю новые данные: {steam_response}\n{steam_response.json()}")
                        if steam_response.status_code == 200:
                            print("Получил данные", type(steam_response.json()))
                            steam_data = steam_response.json()
                            print("Кидаю данные для обновления")
                            update_response = await client.put(f"{GAME_DATA_SERVICE_URL}/game/{appid}", steam_data)
                            print("В теории обновилось")
                            if update_response.status_code not in (200, 204):
                                logger.error(f"Failed to update game data for appid {appid} in Game Data Service")
                            return JSONResponse(content=steam_data)
                        else:
                            print(f"Steam Integration Service вернул {steam_response.status_code}")
                            return JSONResponse(content=game_data)
                    else:
                        print("Данные актуальны, возвращаю из базы")
                        return JSONResponse(content=game_data)
                else:
                    print("Поле updated_at отсутствует, возвращаю данные как есть")
                    return JSONResponse(content=game_data)
            else:
                print("Ошибка при получении данных из Game Data Service")
                raise HTTPException(status_code=response.status_code, detail="Error fetching game data")
        except Exception as e:
            logger.error(f"Error in API Gateway fetching game {appid}: {e}")
            print(f"Блядь, все все сломалось!!! {e}")
            raise HTTPException(status_code=500, detail=str(e))
