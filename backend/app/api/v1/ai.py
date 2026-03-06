from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.db.session import get_db
from app.services.ai_service import AiService
from app.services.stay_service import StayService
from app.services.room_service import RoomService
from app.schemas.stay import ConsumptionCreate, ConsumptionResponse

router = APIRouter()


# Schema apenas para receber o texto livre do Frontend
class AiParseRequest(BaseModel):
    text: str


@router.post(
    "/parse-consumption",
    response_model=List[ConsumptionResponse],
    status_code=status.HTTP_201_CREATED,
)
def parse_and_add_consumption(request: AiParseRequest, db: Session = Depends(get_db)):
    """
    Recebe um texto livre, passa pela IA para extrair os dados e já salva os consumos no banco.
    Fluxo: Texto -> IA -> JSON -> Busca Quarto -> Busca Hospedagem -> Salva Consumos.
    """
    # 1. IA extrai os dados do texto
    try:
        parsed_data = AiService.parse_consumption_text(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    room_number = parsed_data.get("room_number")
    items = parsed_data.get("items", [])

    if not room_number or not items:
        raise HTTPException(
            status_code=400,
            detail="A IA não conseguiu identificar o quarto ou os itens no texto.",
        )

    # 2. Verifica se o quarto existe usando o nosso RoomService
    room = RoomService.get_room_by_number(db, number=room_number)
    if not room:
        raise HTTPException(
            status_code=404, detail=f"Quarto {room_number} não encontrado no sistema."
        )

    # 3. Verifica se tem alguém hospedado lá
    stay = StayService.get_active_stay_by_room(db, room_id=room.id)
    if not stay:
        raise HTTPException(
            status_code=400,
            detail=f"Não há hospedagem ativa no quarto {room_number} para adicionar consumos.",
        )

    # 4. Salva todos os itens mágicamente no banco
    added_consumptions = []
    for item in items:
        consumption_in = ConsumptionCreate(
            stay_id=stay.id,
            item_name=item["item_name"],
            price=item["price"],
            quantity=item["quantity"],
        )
        added_item = StayService.add_consumption(db, consumption_in)
        added_consumptions.append(added_item)

    return added_consumptions
