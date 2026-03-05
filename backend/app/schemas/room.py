# backend/app/schemas/room.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.models.room import RoomStatus


class RoomBase(BaseModel):
    """Base com validações rigorosas de negócio."""

    number: str = Field(..., description="Número/Identificação do quarto (Ex: '101A')")
    capacity: int = Field(..., ge=1, description="Capacidade de hóspedes (Mínimo 1)")
    has_ac: bool = Field(False, description="O quarto possui ar-condicionado?")
    has_breakfast: bool = Field(False, description="A diária inclui café da manhã?")
    status: RoomStatus = Field(default=RoomStatus.FREE)


class RoomCreate(RoomBase):
    """Schema utilizado na criação de um quarto."""

    pass


class RoomResponse(RoomBase):
    """Schema utilizado para retornar dados à interface gráfica."""

    id: UUID

    # Configuração vitalícia do Pydantic V2 para converter objetos ORM em JSON
    model_config = ConfigDict(from_attributes=True)
