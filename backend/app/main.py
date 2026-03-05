from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa o roteador que acabamos de criar
from app.api.v1 import rooms

# Inicializa a aplicação com metadados para o Swagger UI
app = FastAPI(
    title="Renascente Hotel API ☀️⛅",
    description="Web Service interno para gestão de quartos, hospedagens e IA.",
    version="1.0.0",
)

# Configuração rigorosa de CORS (Cross-Origin Resource Sharing)
# Permite que o nosso Frontend (React/Vite na porta 5173) converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Em produção, mudar para o domínio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Acopla as rotas de quartos sob o prefixo padronizado de versão da API
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["Quartos"])


@app.get("/health", tags=["DevOps"])
def health_check():
    """
    Endpoint de observabilidade para verificar se a API está online.
    O Docker ou Load Balancers usarão esta rota.
    """
    return {
        "status": "online",
        "message": "O sol nasceu para a API do Renascente Hotel! ☀️⛅",
    }
