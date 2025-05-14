from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from microservices.api_gateway.routes import router

app = FastAPI(
    title="Steam GeoPricing Inspector API Gateway",
    description="API Gateway для микросервисов Steam GeoPricing Inspector.",
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
