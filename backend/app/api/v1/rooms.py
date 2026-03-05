from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomResponse
from app.models.room import RoomStatus
from app.services.room_service import RoomService

# Inicializa o roteador modular para o domínio de Quartos
router = APIRouter()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    """
    Cria um novo quarto no hotel.
    Bloqueia a criação se o número do quarto já existir (Regra de Negócio).
    """
    existing_room = RoomService.get_room_by_number(db, number=room_in.number)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O quarto com o número {room_in.number} já está registrado.",
        )

    return RoomService.create_room(db=db, room_in=room_in)


@router.get("/", response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
def list_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os quartos cadastrados com paginação opcional.
    """
    return RoomService.get_all_rooms(db=db, skip=skip, limit=limit)


@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_room(room_id: UUID, db: Session = Depends(get_db)):
    """
    Busca os detalhes de um quarto específico pelo seu ID (UUID).
    """
    room = RoomService.get_room_by_id(db=db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quarto não encontrado."
        )
    return room


@router.patch(
    "/{room_id}/status", response_model=RoomResponse, status_code=status.HTTP_200_OK
)
def update_room_status(
    room_id: UUID, new_status: RoomStatus, db: Session = Depends(get_db)
):
    """
    Atualiza apenas a máquina de estados (Status) de um quarto específico.
    """
    room = RoomService.update_room_status(db=db, room_id=room_id, new_status=new_status)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado para atualização.",
        )
    return room
