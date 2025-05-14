from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from microservices.game_data_service import crud, models
from microservices.game_data_service.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/game/{appid}")
def get_game(appid: int, db: Session = Depends(get_db)):
    game = crud.get_game_by_appid(db, appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.data
