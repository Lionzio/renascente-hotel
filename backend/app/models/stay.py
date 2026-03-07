# backend/app/models/stay.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.db.base_class import Base

class Stay(Base):
    __tablename__ = "stays"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    guest_name = Column(String, nullable=False)
    check_in = Column(DateTime, default=datetime.utcnow, nullable=False)
    check_out = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)  # True = Hóspede está no hotel
    total_amount = Column(Float, default=0.0)
    
    # Validador financeiro: O checkout registra a fatura como paga
    is_paid = Column(Boolean, default=False, nullable=False)

    room = relationship("Room")
    consumptions = relationship("Consumption", back_populates="stay", cascade="all, delete-orphan")