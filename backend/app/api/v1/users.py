# backend/app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
from app.api.deps import get_current_super_admin

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_team_member(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """[SUPER_ADMIN] Cadastra novos Gerentes ou Funcionários."""
    user = UserService.get_user_by_name(db, name=user_in.name)
    if user:
        raise HTTPException(
            status_code=400, detail="Já existe um funcionário com este nome."
        )
    return UserService.create_user(db, user_in=user_in)


@router.get("/", response_model=List[UserResponse])
def list_team(
    db: Session = Depends(get_db), current_user=Depends(get_current_super_admin)
):
    """[SUPER_ADMIN] Lista toda a equipa do hotel."""
    return UserService.get_all_users(db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_super_admin),
):
    """[SUPER_ADMIN] Remove um funcionário do sistema."""
    success = UserService.delete_user(db, str(user_id))
    if not success:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
