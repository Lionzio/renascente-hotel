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
        """Busca um quarto específico pelo seu ID."""
        return db.query(Room).filter(Room.id == room_id).first()

    @staticmethod
    def get_room_by_number(db: Session, number: str) -> Optional[Room]:
        """Busca um quarto pelo número (útil para evitar duplicidades na criação)."""
        return db.query(Room).filter(Room.number == number).first()

    @staticmethod
    def get_all_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
        """Retorna a lista de quartos com paginação básica."""
        return db.query(Room).offset(skip).limit(limit).all()

    @staticmethod
    def create_room(db: Session, room_in: RoomCreate) -> Room:
        """
        Cria um novo quarto no sistema.
        Transforma o Schema validado (Pydantic) em um Modelo de Banco (SQLAlchemy).
        """
        # Desempacota os dados validados do Pydantic para criar a instância ORM
        db_room = Room(**room_in.model_dump())

        db.add(db_room)
        db.commit()
        db.refresh(db_room)  # Atualiza o objeto com o ID gerado pelo banco

        return db_room

    @staticmethod
    def update_room_status(
        db: Session, room_id: UUID, new_status: RoomStatus
    ) -> Optional[Room]:
        """
        Atualiza a máquina de estados do quarto.
        Ex: Livre -> Ocupado, ou Ocupado -> A ser arrumado.
        """
        db_room = RoomService.get_room_by_id(db, room_id)
        if not db_room:
            return None

        db_room.status = new_status
        db.commit()
        db.refresh(db_room)

        return db_room
