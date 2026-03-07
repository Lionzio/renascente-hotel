# backend/app/services/stay_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status

from app.models.stay import Stay
from app.models.room import Room, RoomStatus
from app.models.consumption import Consumption
from app.schemas.stay import StayCreate, ConsumptionCreate


class StayService:
    @staticmethod
    def process_checkin(db: Session, stay_in: StayCreate) -> Stay:
        try:
            # BLINDAGEM: Verifica se o quarto existe E se não foi excluído logicamente (Soft Delete)
            room = (
                db.query(Room)
                .filter(Room.id == stay_in.room_id, Room.is_active == True)
                .first()
            )
            if not room:
                raise HTTPException(
                    status_code=404, detail="Quarto não encontrado ou inativo."
                )

            if room.status != RoomStatus.FREE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Check-in bloqueado. O status atual do quarto é: {room.status.value}",
                )

            # O campo is_paid já nasce como False automaticamente pelo modelo do banco de dados
            new_stay = Stay(room_id=stay_in.room_id, guest_name=stay_in.guest_name)
            db.add(new_stay)

            # Muda o estado do quarto e confirma transação
            room.status = RoomStatus.OCCUPIED
            db.commit()
            db.refresh(new_stay)
            return new_stay

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            # Garante que transações corrompidas sejam descartadas
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Erro interno do banco de dados: {str(e)}"
            )

    @staticmethod
    def get_active_stay_by_room(db: Session, room_id: UUID) -> Stay:
        stay = (
            db.query(Stay)
            .filter(Stay.room_id == room_id, Stay.is_active == True)
            .first()
        )
        if not stay:
            raise HTTPException(
                status_code=404, detail="Não há hospedagem ativa neste quarto."
            )
        return stay

    @staticmethod
    def add_consumption(db: Session, consumption_in: ConsumptionCreate) -> Consumption:
        try:
            stay = (
                db.query(Stay)
                .filter(Stay.id == consumption_in.stay_id, Stay.is_active == True)
                .first()
            )
            if not stay:
                raise HTTPException(
                    status_code=400,
                    detail="A hospedagem não existe ou já foi encerrada.",
                )

            new_item = Consumption(**consumption_in.model_dump())
            db.add(new_item)

            # Atualiza o valor total da conta instantaneamente
            stay.total_amount += new_item.price * new_item.quantity
            db.commit()
            db.refresh(new_item)
            return new_item

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Falha ao registrar consumo: {str(e)}"
            )

    @staticmethod
    def process_checkout(db: Session, stay_id: UUID) -> Stay:
        """
        Finaliza a estadia, consolida a conta, MARCA COMO PAGO e libera o quarto para limpeza.
        """
        try:
            stay = (
                db.query(Stay)
                .filter(Stay.id == stay_id, Stay.is_active == True)
                .first()
            )
            if not stay:
                raise HTTPException(
                    status_code=404, detail="Hospedagem não encontrada ou já encerrada."
                )

            # Finaliza a estadia e valida o aspecto financeiro
            stay.is_active = False
            stay.is_paid = True  # <--- AUDITORIA: Confirma a quitação financeira
            stay.check_out = datetime.utcnow()

            # Dispara o gatilho da máquina de estados do quarto para Manutenção/Limpeza
            room = db.query(Room).filter(Room.id == stay.room_id).first()
            if room:
                room.status = RoomStatus.TO_BE_CLEANED

            db.commit()
            db.refresh(stay)
            return stay

        except HTTPException:
            raise
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Falha processar check-out: {str(e)}"
            )
