from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.db.base import Base


class Consumption(Base):
    __tablename__ = "consumptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    stay_id = Column(UUID(as_uuid=True), ForeignKey("stays.id"), nullable=False)
    item_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    stay = relationship("Stay", back_populates="consumptions")
