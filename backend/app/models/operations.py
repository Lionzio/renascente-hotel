# backend/app/models/operations.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base_class import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    salary = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cleanings = relationship("CleaningRecord", back_populates="employee")


class CleaningRecord(Base):
    __tablename__ = "cleaning_records"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    cleaned_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="cleanings")


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    description = Column(String, nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    resolved = Column(Boolean, default=False)


class RoomNote(Base):
    __tablename__ = "room_notes"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    content = Column(String, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
