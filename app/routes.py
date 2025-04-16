from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from app import crud, models
from app.database import get_db
from app.steam import get_info_across_regions  # Update to use the new function
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/doc")
async def doc():
    print(12312424)
    return {"message": "This is a doc endpoint"}

@router.get("/game/{appid}")
async def get_game(appid: int, db: Session = Depends(get_db)):
    
    # Список всех необходимых и стандартных регионов для подтягивания данных
    steam_regions = [ "US", # США 
                     "RU", # Россия 
                     "TR", # Турция 
                     "KZ", # Казахстан
                     #"GB", # Великобритания 
                     #"EU", # Евросоюз (неофициально, использовать DE, FR и т.д.) 
                     #"DE", # Германия 
                     #"FR", # Франция 
                     #"NL", # Нидерланды 
                     #"BR", # Бразилия 
                     #"AR", # Аргентина 
                     #"CL", # Чили 
                     #"MX", # Мексика 
                     #"CN", # Китай 
                     #"JP", # Япония 
                     #"KR", # Южная Корея 
                     #"IN", # Индия 
                     #"ID", # Индонезия 
                     #"TH", # Таиланд 
                     #"UA", # Украина 
                     #"ZA", # ЮАР 
                     #"CA", # Канада 
                     #"AU", # Австралия 
                     #"SG", # Сингапур 
                     #"PH", # Филиппины 
                     #"" # Глобальный (без указания страны, default — USD) 
                     ]
    
    print(steam_regions)
    
    db_game = crud.get_game_by_appid_and_region(db, appid, steam_regions) #Проверка на наличие игры в базе данных 
    print("\n\n\n\n",db_game)
    if db_game == "True":
        game_data = get_info_across_regions(appid=appid, regions=steam_regions)
        print(f"GAME DATA ABOUT {appid}:",game_data,"\n\n\n")
        #Доработать проверку на всякий случай
        #if game_data.get("break"): Сейсач game_data - list поэтому такая проверка не подходит, но если расширение будет парсить url тогда такой ошибки не будет и проверка не нужна
        #    return JSONResponse(status_code=404, content={"error": "Game not found"})
        crud.update_game(db, appid, game_data)
        return game_data
    elif db_game: # Если игра есть в базе данных по все regions
        if db_game.updated_at < datetime.utcnow() - timedelta(minutes=1):#weeks=1
            game_data = get_info_across_regions(appid=appid, regions=steam_regions)
            print("\n\n\n\n",game_data)
            #Добавить обработку исключений
            """if game_data.get("break"):
                return JSONResponse(status_code=404, content={"error": "Game not found"})"""
            crud.update_game(db, appid, game_data)
            return game_data
        return db_game.data
    else: # Если нет игры с такими регионами
        game_data = get_info_across_regions(appid=appid, regions=steam_regions)
        print(f"GAME DATA ABOUT {appid}:",game_data,"\n\n\n")
        #Доработать проверку на всякий случай
        #if game_data.get("break"): Сейсач game_data - list поэтому такая проверка не подходит, но если расширение будет парсить url тогда такой ошибки не будет и проверка не нужна
        #    return JSONResponse(status_code=404, content={"error": "Game not found"})
        crud.create_game(db, appid, game_data, steam_regions)
        return game_data

"""@router.get("/game/{appid}/regions")
async def get_game_multiple_regions(
    appid: int,
    regions: List[str] = Query(..., description="Список регионов, например: ru,us,tr"),
    db: Session = Depends(get_db)
):
    # Collect data for all specified regions
    all_data = get_info_across_regions(appid, regions)
    
    results = []
    for game_data in all_data:
        if game_data.get("break"):
            results.append({"region": game_data["region"], "error": "Game not found"})
        else:
            crud.create_or_update_game(db, appid, game_data)
            results.append({"region": game_data["region"], "data": game_data})
    return results"""
