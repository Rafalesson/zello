import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.crud import crud_agenda
from app.schemas import slot_horario as slot_schema
from .auth import get_current_user_payload

router = APIRouter()

@router.post("/slots", response_model=List[slot_schema.SlotHorarioPublic], status_code=status.HTTP_201_CREATED)
def create_slots_for_medico(
    slots_in: slot_schema.SlotsParaCriacao,
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_payload)
):
    """Cria um ou mais slots de horário na agenda do médico autenticado."""
    # Valida o tipo de usuário usando a string do payload do token
    if current_user_payload.get("tipo_usuario") != "MEDICO":
        raise HTTPException(status_code=403, detail="Apenas médicos podem criar horários.")
        
    medico_id = uuid.UUID(current_user_payload.get("user_id"))
    
    agenda = crud_agenda.get_or_create_agenda(db=db, medico_id=medico_id)
    slots_data = [slot.model_dump() for slot in slots_in.slots]
    return crud_agenda.create_slots_para_agenda(db=db, agenda=agenda, slots_data=slots_data)

@router.get("/medico/{medico_id}", response_model=List[slot_schema.SlotHorarioPublic])
def get_agenda_disponivel_de_medico(
    medico_id: uuid.UUID,
    data: Optional[datetime.date] = None,
    db: Session = Depends(get_db)
):
    """Retorna uma lista de slots de horário disponíveis para um médico."""
    return crud_agenda.get_slots_disponiveis(db=db, medico_id=medico_id, data=data)