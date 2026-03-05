from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.stay import (
    StayCreate,
    StayResponse,
    ConsumptionCreate,
    ConsumptionResponse,
)
from app.services.stay_service import StayService

router = APIRouter()


@router.post(
    "/checkin", response_model=StayResponse, status_code=status.HTTP_201_CREATED
)
def checkin_guest(stay_in: StayCreate, db: Session = Depends(get_db)):
    """Inicia a estadia e muda o quarto para OCUPADO."""
    return StayService.process_checkin(db=db, stay_in=stay_in)


@router.post(
    "/consumption",
    response_model=ConsumptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_guest_consumption(
    consumption_in: ConsumptionCreate, db: Session = Depends(get_db)
):
    """Adiciona um item consumido à conta do hóspede."""
    return StayService.add_consumption(db=db, consumption_in=consumption_in)


@router.post(
    "/{stay_id}/checkout", response_model=StayResponse, status_code=status.HTTP_200_OK
)
def checkout_guest(stay_id: UUID, db: Session = Depends(get_db)):
    """Encerra a estadia, fecha a conta e muda o quarto para A ARRUMAR."""
    return StayService.process_checkout(db=db, stay_id=stay_id)


@router.get(
    "/room/{room_id}/active",
    response_model=StayResponse,
    status_code=status.HTTP_200_OK,
)
def get_current_guest(room_id: UUID, db: Session = Depends(get_db)):
    """Retorna os dados da hospedagem ativa de um quarto."""
    return StayService.get_active_stay_by_room(db=db, room_id=room_id)
