from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models
from app.database import get_db
from app.steam import get_info_across_regions  # Update to use the new function
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/doc")
async def doc():
    return {"message": "This is a doc endpoint"}

@router.get("/game/{appid}")
async def get_game(appid: int, db: AsyncSession = Depends(get_db)):
    steam_regions = ["US", "RU", "TR", "KZ"]
    
    db_game = await crud.get_game_by_appid_and_region(db, appid, steam_regions)  # Use async CRUD function
    if db_game == "True":
        game_data = await get_info_across_regions(appid=appid, regions=steam_regions)
        await crud.update_game(db, appid, game_data)  # Use async update
        return game_data
    elif db_game:  # If the game exists in the database for all regions
        if db_game.updated_at < datetime.utcnow() - timedelta(minutes=1):
            game_data = await get_info_across_regions(appid=appid, regions=steam_regions)
            await crud.update_game(db, appid, game_data)  # Use async update
            return game_data
        return db_game.data
    else:  # If no game with those regions
        game_data = await get_info_across_regions(appid=appid, regions=steam_regions)
        await crud.create_game(db, appid, game_data, steam_regions)  # Use async create
        return game_data
