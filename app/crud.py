from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
from typing import List
from app.models import Game

def get_game_by_appid(db: Session, appid: int):
    """
    Получить игру из базы данных по её appid.
    Возвращает объект игры или None, если игра не найдена.
    """
    return db.query(models.Game).filter(models.Game.appid == appid).first()

def get_game_by_appid_and_region(db: Session, appid: int, regions: List[str] = ["ru"]):
    """
    Проверить наличие игры в базе данных для указанных регионов.
    Возвращает объект игры, если данные по всем регионам есть.
    Возвращает пустой список, если игра отсутствует.
    Возвращает строку "True", если игра есть, но не для всех регионов.
    """
    game = get_game_by_appid(db, appid)
    if not game:
        return []

    data_row = game.data  # это jsonb словарь
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
                return e_flag  # если игры нет в базе данных по региону
            return []  # если игры нет в базе данных по региону
    return game

def update_game(db: Session, appid: int, game_data: dict):
    """
    Обновить данные игры в базе по appid.
    Обновляет поле data и время обновления.
    Возвращает обновлённый объект игры.
    """
    db_game = get_game_by_appid(db, appid)
    if db_game:
        db_game.data = game_data
        db_game.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_game)
        return db_game
    return None

def create_game(db: Session, appid: int, game_data: list, regions: List[str]):
    """
    Создать новые записи игры в базе данных для каждого региона.
    Возвращает список созданных объектов игры.
    """
    print("я зашел")
    created_games = []

    for region in regions:
        new_game = models.Game(
            appid=appid,
            data=game_data,
            updated_at=datetime.utcnow(),
        )
    print("добавляю")
    db.add(new_game)
    print("добавил")


    created_games.append(new_game)

    db.commit()

    for game in created_games:
        db.refresh(game)
        print("я вышел")

    return created_games
