# backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import bcrypt
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto limpo bate com o hash salvo no banco."""
    # O bcrypt exige que as strings sejam convertidas para bytes (utf-8)
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    """Gera o hash irreversível da senha com um salt aleatório."""
    # Gera o hash em bytes e depois decodifica para string para salvar no banco
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera o Token JWT para o usuário."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
