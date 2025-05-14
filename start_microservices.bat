@echo off
REM Запускаем три консоли в разные края экрана, чтобы не накладывались

start "" cmd /k "title Game Data Service & uvicorn microservices.game_data_service.main:app --port 8001 --reload"
timeout /t 1 /nobreak >nul

start "" cmd /k "title Steam Integration Service & uvicorn microservices.steam_integration_service.main:app --port 8002 --reload"
timeout /t 1 /nobreak >nul

start "" cmd /k "title API Gateway & uvicorn microservices.api_gateway.main:app --port 8000 --reload"
