# backend/app/services/room_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from app.models.room import Room, RoomStatus
from app.schemas.room import RoomCreate


class RoomService:
    """
    Camada de Serviço para Quartos.
    Isola a lógica de negócio e as consultas ao banco de dados das rotas HTTP.
    """

    @staticmethod
    def get_room_by_id(db: Session, room_id: UUID) -> Optional[Room]:
        return db.query(Room).filter(Room.id == room_id).first()

    @staticmethod
    def get_room_by_number(db: Session, number: str) -> Optional[Room]:
        return db.query(Room).filter(Room.number == number).first()

    @staticmethod
    def get_all_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
        return db.query(Room).offset(skip).limit(limit).all()

    @staticmethod
    def create_room(db: Session, room_in: RoomCreate) -> Room:
        db_room = Room(**room_in.model_dump())
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def update_room_status(
        db: Session, room_id: UUID, new_status: RoomStatus
    ) -> Optional[Room]:
        db_room = RoomService.get_room_by_id(db, room_id)
        if not db_room:
            return None
        db_room.status = new_status
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def update_room(db: Session, room_id: UUID, room_in: RoomCreate) -> Optional[Room]:
        """Atualiza as características físicas de um quarto."""
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return None
        room.number = room_in.number
        room.capacity = room_in.capacity
        room.has_ac = room_in.has_ac
        room.has_breakfast = room_in.has_breakfast
        db.commit()
        db.refresh(room)
        return room

    @staticmethod
    def delete_room(db: Session, room_id: UUID) -> bool:
        """Exclui o quarto se não houver conflitos de chave estrangeira (histórico)."""
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if not room:
                return False
            db.delete(room)
            db.commit()
            return True
        except Exception:
            db.rollback()
            # Erro comum se houver hospedagens atreladas ao quarto no banco
            raise ValueError(
                "Não é possível excluir um quarto que possui histórico de hospedagens ou faturas atreladas."
            )
