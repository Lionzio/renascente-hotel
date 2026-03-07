from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações globais da API.

    Boas Práticas: O Pydantic lê automaticamente as variáveis de ambiente
    do Sistema Operacional. Como estamos usando Docker, o 'docker-compose.yml'
    (via env_file) é o único responsável por injetar essas variáveis de forma segura no container.
    """

    PROJECT_NAME: str = "Renascente Hotel API ☀️⛅"
    DATABASE_URL: str
    GEMINI_API_KEY: str = ""


# Instância global das configurações para ser importada em toda a aplicação
settings = Settings()
