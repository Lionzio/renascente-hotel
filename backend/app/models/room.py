# backend/app/models/room.py
import enum
import uuid
from sqlalchemy import Column, String, Integer, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class RoomStatus(str, enum.Enum):
    """Máquina de Estados rigorosa para o ciclo de vida do quarto."""

    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    TO_BE_CLEANED = "TO_BE_CLEANED"
    TO_BE_VACATED = "TO_BE_VACATED"
    MAINTENANCE = "MAINTENANCE"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    number = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    has_ac = Column(Boolean, default=False, nullable=False)
    has_breakfast = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.FREE, nullable=False)

    # Soft Delete: Mantém o histórico no banco, mas oculta da aplicação
    is_active = Column(Boolean, default=True, nullable=False)
