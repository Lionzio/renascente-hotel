# backend/app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importação dos roteadores de cada domínio
from app.api.v1 import rooms, stays, ai, auth, users
from app.core.config import settings

# --- CONFIGURAÇÃO DE LOGS (BOA PRÁTICA) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("renascente_api")

# --- DEDO-DURO PARA DEBUG DA CHAVE GEMINI (BLINDADO) ---
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

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Renascente Hotel API ☀️⛅",
    description="Web Service interno para gestão de quartos, hospedagens, equipa e IA.",
    version="1.1.0",
)

# --- CONFIGURAÇÃO DE CORS ---
# Permite que o Frontend (React/Vite rodando na porta 5173) consiga comunicar-se com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PATCH, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- REGISTRO DE ROTAS (ROUTERS) ---
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(
    users.router, prefix="/api/v1/users", tags=["Gestão de Equipa (Super Admin)"]
)
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["Quartos"])
app.include_router(stays.router, prefix="/api/v1/stays", tags=["Hospedagens"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["Cérebro IA"])


# --- ROTA DE HEALTH CHECK ---
@app.get("/health", tags=["DevOps"])
def health_check():
    """Endpoint para verificação de saúde (Health Check) do Docker."""
    return {
        "status": "online",
        "message": "O sol nasceu para a API do Renascente Hotel! ☀️⛅",
    }
