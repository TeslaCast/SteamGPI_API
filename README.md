
# SteamGPI API
Сервис для мониторинга цен и доступности игр в Steam по регионам.

## Обзор
Steam GeoPricing Inspector API позволяет получать информацию о ценах и доступности игр в Steam в разных регионах. Этот API полезен для сравнения цен и проверки региональной доступности прямо из браузерного расширения.

## 📌 Цели проекта
- Проверка актуальных цен на игры в Steam по регионам.
- Сравнение скидок и цен в разных валютах.
- Хранение информации об играх в PostgreSQL в формате JSONB.
- Расширяемость.

## ⚙️ Технологии
- Python (основной парсер и API-клиент)
- PostgreSQL (база данных)
- JSONB (гибкое хранение данных)
- Docker (контейнеризация)
- Git + Git Hooks + линтеры (code quality)
- Steam Store API

## 🗄 Структура БД

### Таблица: games

| Поле        | Тип         | Описание                                   |
|-------------|-------------|--------------------------------------------|
| appid       | INTEGER     | ID игры в Steam (primary key)              |
| data        | JSONB       | Вся информация об игре и ценах по регионам |
| updated_at  | TIMESTAMP   | Время последнего обновления                |

### Таблица: users

| Поле        | Тип         | Описание                                   |
|-------------|-------------|--------------------------------------------|
| userid      | INTEGER     | ID пользователя (primary key)              |
| login       | CHAR        | Login пользователя                         |
| password    | TIMESTAMP   | Password  пользователя                     |

### Таблица: alerts

| Поле        | Тип         | Описание                                   |
|-------------|-------------|--------------------------------------------|
| alertid     | INTEGER     | ID уведомления                             |
| userid      | INTEGER     | ID пользователя                            |
| appid       | INTEGER     | ID игр                                     |
| price       | INTEGER     | Цена игры в момент уведомления             |


## Базовый URL
https://store.steampowered.com/api/appdetails

## Эндпоинты

### 1. Получение информации об игре в одном регионе
Возвращает данные о цене и доступности игры в указанном регионе.

**Эндпоинт:**
GET /game/{appid}

**Параметры:**
- `appid` (integer, обязательно) – Уникальный идентификатор игры в Steam.
- `region` (string, опционально) – Код региона (например, ru, us, tr). Если не указан, возвращается глобальная информация.
- `language` (string, опционально) – Язык описания игры (например, en, ru).

**Ответ:**
JSON-объект с информацией о продукте.

#### Пример запроса:
GET /game/632360?region=us&language=en

#### Пример ответа:
```json
{
  "appid": 632360,
  "region": "us",
  "name": "Risk of Rain 2",
  "available": true,
  "initial_price": 24.99,
  "final_price": 24.99,
  "currency": "USD",
  "discount_percent": 0
}
```

---

### 2. Получение информации об игре в нескольких регионах
Возвращает данные о цене и доступности игры в нескольких регионах.

**Эндпоинт:**
GET /game/{appid}/regions

**Параметры:**
- `appid` (integer, обязательно) – Уникальный идентификатор игры в Steam.
- `regions` (массив строк, обязательно) – Список кодов регионов (например, ru,us,eu,tr).

**Ответ:**
JSON-массив с информацией по каждому региону.

#### Пример запроса:
GET /game/3159330/regions?regions=ru,us

#### Пример ответа:
```json
[
  {
    "appid": 3159330,
    "region": "ru",
    "name": "Assassin’s Creed Shadows",
    "available": false
  },
  {
    "appid": 3159330,
    "region": "us",
    "name": "Assassin’s Creed Shadows",
    "available": true,
    "initial_price": 69.99,
    "final_price": 69.99,
    "currency": "USD",
    "discount_percent": 0
  }
]
```

## Обработка ошибок
- 400 Bad Request – Неверный запрос (например, отсутствует appid).
- 404 Not Found – Игра не найдена.
- 500 Internal Server Error – Внутренняя ошибка сервера.

## Ограничения
API ограничено 60 запросами в минуту на один IP-адрес.
