@echo off
start cmd /k "uvicorn microservices.game_data_service.main:app --port 8001 --reload"
start cmd /k "uvicorn microservices.steam_integration_service.main:app --port 8002 --reload"
start cmd /k "uvicorn microservices.api_gateway.main:app --port 8000 --reload"
