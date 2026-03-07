# backend/app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações globais da API.
    As variáveis de ambiente são lidas automaticamente pelo Pydantic.
    """

    PROJECT_NAME: str = "Renascente Hotel API ☀️⛅"
    DATABASE_URL: str
    GEMINI_API_KEY: str = ""

    # Variáveis de Segurança JWT (Para produção, estas chaves devem vir do .env)
    SECRET_KEY: str = "renascente_hotel_super_secreta_chave_2026_dev_mode"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # Token dura 7 dias (útil em testes)


# Instância global das configurações para ser importada em toda a aplicação
settings = Settings()
