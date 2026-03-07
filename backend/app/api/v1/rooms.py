# backend/app/api/v1/rooms.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomResponse
from app.models.room import RoomStatus
from app.services.room_service import RoomService
from app.schemas.operations import (
    CleaningCreate,
    MaintenanceCreate,
    NoteCreate,
    NoteResponse,
)
from app.models.operations import Employee, CleaningRecord, MaintenanceRecord, RoomNote

# Importação dos Guardas de Rota de Segurança atualizados
from app.api.deps import get_current_user, get_current_manager
from app.models.user import User

router = APIRouter()

# =======================================================
# OPERAÇÕES CRUD DE QUARTOS
# =======================================================


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    """[GERENTE/SUPER ADMIN] Cria um novo quarto no sistema."""
    existing_room = RoomService.get_room_by_number(db, number=room_in.number)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O quarto {room_in.number} já existe.",
        )
    return RoomService.create_room(db=db, room_in=room_in)


@router.get("/", response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
def list_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Lista todos os quartos visíveis (Soft Delete respeitado)."""
    return RoomService.get_all_rooms(db=db, skip=skip, limit=limit)


@router.get("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def get_room(
    room_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Retorna as informações de um quarto específico."""
    room = RoomService.get_room_by_id(db=db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quarto não encontrado."
        )
    return room


@router.patch(
    "/{room_id}/status", response_model=RoomResponse, status_code=status.HTTP_200_OK
)
def update_room_status(
    room_id: UUID,
    new_status: RoomStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Altera o status da máquina de estados do quarto."""
    room = RoomService.update_room_status(db=db, room_id=room_id, new_status=new_status)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quarto não encontrado."
        )
    return room


@router.put("/{room_id}", response_model=RoomResponse, status_code=status.HTTP_200_OK)
def update_room(
    room_id: UUID,
    room_in: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    """[GERENTE/SUPER ADMIN] Edita características físicas do quarto."""
    room = RoomService.update_room(db=db, room_id=room_id, room_in=room_in)
    if not room:
        raise HTTPException(status_code=404, detail="Quarto não encontrado.")
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_manager),
):
    """[GERENTE/SUPER ADMIN] Aplica o Soft Delete num quarto, desde que sem pendências."""
    try:
        success = RoomService.delete_room(db=db, room_id=room_id)
        if not success:
            raise HTTPException(status_code=404, detail="Quarto não encontrado.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =======================================================
# ROTAS OPERACIONAIS (Arrumação, Manutenção e Notas)
# =======================================================


@router.post("/{room_id}/clean", status_code=status.HTTP_200_OK)
def register_cleaning(
    room_id: UUID,
    cleaning: CleaningCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Regista a limpeza e libera o quarto."""
    emp = db.query(Employee).filter(Employee.name == cleaning.employee_name).first()
    if not emp:
        emp = Employee(name=cleaning.employee_name, salary=1500.0)
        db.add(emp)
        db.commit()
        db.refresh(emp)

    record = CleaningRecord(
        room_id=str(room_id),
        employee_id=emp.id,
        cleaned_at=cleaning.cleaned_at or datetime.utcnow(),
    )
    db.add(record)
    RoomService.update_room_status(db, room_id, RoomStatus.FREE)
    db.commit()
    return {"message": "Limpeza registrada com sucesso."}


@router.post("/{room_id}/maintenance", status_code=status.HTTP_201_CREATED)
def schedule_maintenance(
    room_id: UUID,
    maint: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Coloca o quarto em manutenção e registra o custo."""
    record = MaintenanceRecord(room_id=str(room_id), **maint.model_dump())
    db.add(record)
    RoomService.update_room_status(db, room_id, RoomStatus.MAINTENANCE)
    db.commit()
    return {"message": "Manutenção agendada com sucesso."}


@router.post("/{room_id}/notes", response_model=NoteResponse)
def add_room_note(
    room_id: UUID,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Adiciona aviso/nota ao quarto."""
    new_note = RoomNote(room_id=str(room_id), content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/{room_id}/notes", response_model=List[NoteResponse])
def get_room_notes(
    room_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Lista anotações ativas do quarto."""
    return db.query(RoomNote).filter(RoomNote.room_id == str(room_id)).all()


@router.patch("/{room_id}/notes/{note_id}/resolve")
def resolve_room_note(
    room_id: UUID,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """[QUALQUER FUNCIONÁRIO] Arquiva uma anotação."""
    note = db.query(RoomNote).filter(RoomNote.id == note_id).first()
    if note:
        note.is_resolved = True
        db.commit()
    return {"message": "Anotação resolvida."}
