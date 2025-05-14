from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from microservices.game_data_service.routes import router

app = FastAPI(
    title="Game Data Service",
    description="Микросервис для работы с данными игр и базой данных.",
    version="1.0.0"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
