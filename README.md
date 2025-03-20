# SteamGPI_API
from pathlib import Path

readme_content = """
# Steam Discount Tracker  

Сервис для мониторинга цен и доступности игр в Steam по регионам.

Проект реализован в рамках учебной работы и предназначен для получения информации о ценах, скидках и доступности игр в разных странах с использованием Steam Store API.

## 📌 Цели проекта
- Проверка актуальных цен на игры в Steam по регионам.
- Сравнение скидок и цен в разных валютах.
- Хранение информации об играх в PostgreSQL в формате JSONB.
- Расширяемость для добавления новых функций и площадок.

## ⚙️ Технологии
- Python (основной парсер и API-клиент)
- PostgreSQL (база данных)
- JSONB (гибкое хранение данных)
- Docker (контейнеризация)
- Git + Git Hooks + линтеры (code quality)
- Steam Store API

## 🏗 Структура проекта
- /parser — скрипты для получения данных из Steam API
- /db — SQL-файлы со структурой базы данных
- /api — REST API (при необходимости, реализуем на FastAPI)
- /docs — документация и схемы проекта

## 🗄 Структура БД

Таблица: games

| Поле        | Тип         | Описание                                   |
|-------------|-------------|--------------------------------------------|
| appid       | INTEGER     | ID игры в Steam (primary key)              |
| data        | JSONB       | Вся информация об игре и ценах по регионам|
| updated_at  | TIMESTAMP   | Время последнего обновления                |

Пример содержимого поля data:

```json
{
  "name": "Counter-Strike 2",
  "is_free": false,
  "regions": {
    "ru": {
      "currency": "RUB",
      "initial_price": 1499,
      "final_price": 899,
      "discount_percent": 40
    },
    "us": {
      "currency": "USD",
      "initial_price": 29.99,
      "final_price": 29.99,
      "discount_percent": 0
    },
    "tr": null
  }
}
