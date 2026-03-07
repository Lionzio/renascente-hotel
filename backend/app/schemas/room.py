# backend/app/schemas/room.py
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from app.models.room import RoomStatus

class RoomBase(BaseModel):
    number: str = Field(..., description="Número/Identificação do quarto (Ex: '101A')")
    capacity: int = Field(..., ge=1, description="Capacidade de hóspedes (Mínimo 1)")
    has_ac: bool = Field(False, description="O quarto possui ar-condicionado?")
    has_breakfast: bool = Field(False, description="A diária inclui café da manhã?")
    status: RoomStatus = Field(default=RoomStatus.FREE)
    is_active: bool = Field(default=True, description="Indica se o quarto foi excluído logicamente.")

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)