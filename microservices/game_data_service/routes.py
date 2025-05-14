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
    steam_regions = ["US", "RU", "TR", "KZ"]
    print(f"Хочу найти игру: {appid}")
    game = crud.get_game_by_appid_and_region(db, appid, steam_regions)

    if game =="True":
        print("Нашел игру, но не для всех регионов!")
    elif game:
        print("Игру нашел, возвращаю её")
        return game.data
    else:
        print("Игра не найдена")
        raise HTTPException(status_code=404, detail="Game not found")        
    
    
