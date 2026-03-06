from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import rooms, stays, ai

app = FastAPI(
    title="Renascente Hotel API ☀️⛅",
    description="Web Service interno para gestão de quartos, hospedagens e IA.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["Quartos"])
app.include_router(stays.router, prefix="/api/v1/stays", tags=["Hospedagens"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["Cérebro IA"])


@app.get("/health", tags=["DevOps"])
def health_check():
    return {
        "status": "online",
        "message": "O sol nasceu para a API do Renascente Hotel! ☀️⛅",
    }
