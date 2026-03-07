# backend/app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais de autenticação.",
        )

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return user


def get_current_manager(current_user: User = Depends(get_current_user)) -> User:
    """[RBAC] Permite acesso a GERENTES e SUPER_ADMINS."""
    if current_user.role not in [UserRole.MANAGER, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso Negado: Apenas a Gerência pode executar esta ação.",
        )
    return current_user


def get_current_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """[RBAC] Permite acesso EXCLUSIVO aos donos do sistema."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso Negado: Apenas Administradores Supremos possuem esta permissão.",
        )
    return current_user
