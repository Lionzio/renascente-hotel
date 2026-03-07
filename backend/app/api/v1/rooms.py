from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomResponse
from app.models.room import RoomStatus
from app.services.room_service import RoomService

router = APIRouter()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    existing_room = RoomService.get_room_by_number(db, number=room_in.number)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O quarto {room_in.number} já existe.",
        )
    return RoomService.create_room(db=db, room_in=room_in)


@router.get("/", response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
def list_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return RoomService.get_all_rooms(db=db, skip=skip, limit=limit)


@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_room(room_id: UUID, db: Session = Depends(get_db)):
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
    room = RoomService.update_room_status(db=db, room_id=room_id, new_status=new_status)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quarto não encontrado."
        )
    return room


@router.put("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def update_room(room_id: UUID, room_in: RoomCreate, db: Session = Depends(get_db)):
    room = RoomService.update_room(db=db, room_id=room_id, room_in=room_in)
    if not room:
        raise HTTPException(status_code=404, detail="Quarto não encontrado.")
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    try:
        success = RoomService.delete_room(db=db, room_id=room_id)
        if not success:
            raise HTTPException(status_code=404, detail="Quarto não encontrado.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
