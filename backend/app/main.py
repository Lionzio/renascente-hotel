import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import rooms, stays, ai
from app.core.config import settings

# --- CONFIGURAÇÃO DE LOGS (BOA PRÁTICA) ---
# Utilizar o logger nativo garante que as mensagens não se percam no buffer do Docker
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("renascente_api")

# --- DEDO-DURO PARA DEBUG DA CHAVE (BLINDADO) ---
# Extrai os 5 primeiros caracteres da chave de forma segura, evitando erros se a string for nula
raw_key = settings.GEMINI_API_KEY
if raw_key and len(raw_key.strip()) > 0:
    safe_key = raw_key.strip()[:5]
    print(f"🚀 [DEBUG] Chave Gemini carregada no container começa com: {safe_key}***")
    logger.info(f"Chave Gemini inicializada com prefixo: {safe_key}***")
else:
    print("⚠️ [AVISO CRÍTICO] Nenhuma chave GEMINI_API_KEY foi encontrada no ambiente!")
    logger.warning(
        "Nenhuma chave GEMINI_API_KEY carregada na inicialização do Uvicorn."
    )
# ------------------------------------------------

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Renascente Hotel API ☀️⛅",
    description="Web Service interno para gestão de quartos, hospedagens e Cérebro IA.",
    version="1.0.0",
)

# --- CONFIGURAÇÃO DE CORS ---
# Permite que o Frontend (React/Vite rodando na porta 5173) consiga se comunicar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PATCH, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- REGISTRO DE ROTAS (ROUTERS) ---
# Modularização das rotas para manter o main.py limpo e focado
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["Quartos"])
app.include_router(stays.router, prefix="/api/v1/stays", tags=["Hospedagens"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["Cérebro IA"])


# --- ROTA DE HEALTH CHECK ---
@app.get("/health", tags=["DevOps"])
def health_check():
    """
    Endpoint para verificação de saúde da API.
    Útil para o Docker saber se o container inicializou com sucesso.
    """
    return {
        "status": "online",
        "message": "O sol nasceu para a API do Renascente Hotel! ☀️⛅",
    }
