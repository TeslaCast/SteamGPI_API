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

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("app.routes")

def log_to_db(db: Session, level: str, message: str):
    log_entry = models.Logger(level=level, message=message)
    db.add(log_entry)
    db.commit()

@router.get("/game/{appid}")
async def get_game(appid: int, db: Session = Depends(get_db)):
    steam_regions = ["US", "RU", "TR", "KZ"]
    db_game = crud.get_game_by_appid_and_region(db, appid, steam_regions)

    if db_game == "True":
        try:
            game_data = get_info_across_regions(appid=appid, regions=steam_regions)
            if any(item.get("break") for item in game_data):
                logger.warning(f"Game not found for appid {appid} in some regions")
                log_to_db(db, "WARNING", f"Game not found for appid {appid} in some regions")
                return JSONResponse(status_code=404, content={"error": "Game not found"})
            crud.update_game(db, appid, game_data)
            return game_data
        except Exception as e:
            logger.error(f"Error updating game {appid}: {e}")
            log_to_db(db, "ERROR", f"Error updating game {appid}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    elif db_game:
        if db_game.updated_at < datetime.utcnow() - timedelta(minutes=1):
            try:
                game_data = get_info_across_regions(appid=appid, regions=steam_regions)
                if any(item.get("break") for item in game_data):
                    logger.warning(f"Game not found for appid {appid} in some regions")
                    log_to_db(db, "WARNING", f"Game not found for appid {appid} in some regions")
                    return JSONResponse(status_code=404, content={"error": "Game not found"})
                crud.update_game(db, appid, game_data)
                return game_data
            except Exception as e:
                logger.error(f"Error updating game {appid}: {e}")
                log_to_db(db, "ERROR", f"Error updating game {appid}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        return db_game.data
    else:
        try:
            game_data = get_info_across_regions(appid=appid, regions=steam_regions)
            if any(item.get("break") for item in game_data):
                logger.warning(f"Game not found for appid {appid} in some regions")
                log_to_db(db, "WARNING", f"Game not found for appid {appid} in some regions")
                return JSONResponse(status_code=404, content={"error": "Game not found"})
            crud.create_game(db, appid, game_data, steam_regions)
            return game_data
        except Exception as e:
            logger.error(f"Error creating game {appid}: {e}")
            log_to_db(db, "ERROR", f"Error creating game {appid}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

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
