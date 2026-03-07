# backend/app/services/room_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from app.models.room import Room, RoomStatus
from app.models.stay import Stay
from app.schemas.room import RoomCreate

class RoomService:
    """Camada de Serviço para a gestão do ciclo de vida dos Quartos."""

    @staticmethod
    def get_room_by_id(db: Session, room_id: UUID) -> Optional[Room]:
        return db.query(Room).filter(Room.id == room_id, Room.is_active == True).first()

    @staticmethod
    def get_room_by_number(db: Session, number: str) -> Optional[Room]:
        return db.query(Room).filter(Room.number == number, Room.is_active == True).first()

    @staticmethod
    def get_all_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
        # Retorna apenas os quartos ativos (Soft Delete aplicado)
        return db.query(Room).filter(Room.is_active == True).order_by(Room.number).offset(skip).limit(limit).all()

    @staticmethod
    def create_room(db: Session, room_in: RoomCreate) -> Room:
        db_room = Room(**room_in.model_dump())
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def update_room_status(db: Session, room_id: UUID, new_status: RoomStatus) -> Optional[Room]:
        db_room = RoomService.get_room_by_id(db, room_id)
        if not db_room:
            return None
        db_room.status = new_status
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def update_room(db: Session, room_id: UUID, room_in: RoomCreate) -> Optional[Room]:
        room = RoomService.get_room_by_id(db, room_id)
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
        """Executa um Soft Delete com regras estritas de auditoria financeira e operacional."""
        try:
            room = db.query(Room).filter(Room.id == room_id, Room.is_active == True).first()
            if not room:
                return False
            
            # REGRA 1 (Operacional): Bloqueia exclusão APENAS se houver um hóspede no quarto
            if room.status == RoomStatus.OCCUPIED:
                raise ValueError("Não é possível excluir um quarto que está atualmente ocupado por um hóspede.")
            
            # REGRA 2 (Auditoria Financeira): Garante que não haja faturas em aberto no histórico do quarto
            unpaid_stays = db.query(Stay).filter(Stay.room_id == room_id, Stay.is_paid == False).count()
            if unpaid_stays > 0:
                raise ValueError("Operação bloqueada: Este quarto possui faturas antigas com pagamento pendente.")
            
            # Aplica o Soft Delete (Oculta o quarto da aplicação, preservando os logs no banco)
            room.is_active = False
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise ValueError(str(e))