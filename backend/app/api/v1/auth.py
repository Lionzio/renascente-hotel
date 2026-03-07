# backend/app/api/v1/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas.user import UserResponse, Token
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """O form_data.username contém o NOME inserido no Frontend"""
    user = UserService.get_user_by_name(db, name=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Nome de funcionário ou senha incorretos."
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
