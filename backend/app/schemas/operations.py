from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Funcionários e Limpeza ---
class CleaningCreate(BaseModel):
    employee_name: str
    cleaned_at: Optional[datetime] = None  # Aceita a data enviada pelo frontend


# --- Manutenção ---
class MaintenanceCreate(BaseModel):
    description: str
    scheduled_date: datetime
    estimated_cost: float


class MaintenanceResponse(MaintenanceCreate):
    id: int
    resolved: bool

    class Config:
        from_attributes = True


# --- Anotações ---
class NoteCreate(BaseModel):
    content: str


class NoteResponse(NoteCreate):
    id: int
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True
