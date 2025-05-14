from sqlalchemy.orm import Session
from typing import List
from microservices.game_data_service import models
from datetime import datetime


def get_game_by_appid(db: Session, appid: int):
    return db.query(models.Game).filter(models.Game.appid == appid).first()

def get_game_by_appid_and_region(db: Session, appid: int, regions: List[str] = ["ru"]):
    game = get_game_by_appid(db, appid)
    if not game:
        return []

    data_row = game.data
    data = data_row if isinstance(data_row, list) else [data_row]
    e_flag = "False"
    for region in regions:
        flag = False
        for i in data:
            if i['region'] == region:
                e_flag = "True"
                flag = True
                break

        if not flag:
            if e_flag == "True":
                return e_flag
            return []
    return game

def update_game(db: Session, appid: int, game_data: dict):
    db_game = get_game_by_appid(db, appid)
    if db_game:
        db_game.data = game_data
        db_game.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_game)
        return db_game
    return None

def create_game(db: Session, appid: int, game_data: list, regions: List[str]):
    created_games = []

    for region in regions:
        new_game = models.Game(
            appid=appid,
            data=game_data,
            updated_at=datetime.utcnow(),
        )
        db.add(new_game)
        created_games.append(new_game)

    db.commit()

    for game in created_games:
        db.refresh(game)

    return created_games
