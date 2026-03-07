# backend/app/schemas/stay.py
# (Adicione o is_paid no Response, mantenha o resto do arquivo igual)
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class ConsumptionBase(BaseModel):
    item_name: str
    price: float = Field(gt=0, description="O preço deve ser maior que zero")
    quantity: int = Field(default=1, gt=0)


class ConsumptionCreate(ConsumptionBase):
    stay_id: UUID


class ConsumptionResponse(ConsumptionBase):
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True


class StayCreate(BaseModel):
    room_id: UUID
    guest_name: str = Field(..., min_length=2)


class StayResponse(BaseModel):
    id: UUID
    room_id: UUID
    guest_name: str
    check_in: datetime
    check_out: Optional[datetime] = None
    is_active: bool
    total_amount: float
    is_paid: bool  # NOVO: Reflete no frontend se foi pago
    consumptions: List[ConsumptionResponse] = []

    class Config:
        from_attributes = True
