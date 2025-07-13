# app/api/v1/routes/agendas.py
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.crud import crud_agenda
from app.schemas import slot_horario as slot_schema
from app.schemas import agenda as agenda_schema

router = APIRouter()

# --- Placeholder para a dependência de segurança ---
def get_current_active_medico_placeholder():
    """ATENÇÃO: Este é um placeholder para testes. Retorna um ID de médico fixo."""
    return {"medico_id": uuid.UUID("b63698e3-99b7-4128-9029-d0e5b0387e39")} 
# -------------------------------------------

# CORREÇÃO: O caminho agora é apenas "/medico/{medico_id}"
@router.get(
    "/medico/{medico_id}",
    response_model=List[slot_schema.SlotHorarioPublic],
    summary="Busca horários disponíveis de um médico"
)
def get_agenda_disponivel_de_medico(
    medico_id: uuid.UUID,
    data: Optional[datetime.date] = None,
    db: Session = Depends(get_db)
):
    """
    Retorna uma lista de slots de horário disponíveis para um médico.
    """
    slots = crud_agenda.get_slots_disponiveis(db=db, medico_id=medico_id, data=data)
    return slots

# CORREÇÃO: O caminho agora é apenas "/slots"
@router.post(
    "/slots",
    response_model=List[slot_schema.SlotHorarioPublic],
    status_code=status.HTTP_201_CREATED,
    summary="Cria múltiplos slots de horário para um médico"
)
def create_slots_for_medico(
    slots_in: slot_schema.SlotsParaCriacao,
    db: Session = Depends(get_db),
    current_medico: dict = Depends(get_current_active_medico_placeholder)
):
    """
    Cria um ou mais slots de horário na agenda do médico autenticado.
    """
    medico_id = current_medico["medico_id"]
    agenda = crud_agenda.get_or_create_agenda(db=db, medico_id=medico_id)
    slots_data = [slot.model_dump() for slot in slots_in.slots]
    slots_criados = crud_agenda.create_slots_para_agenda(
        db=db, agenda=agenda, slots_data=slots_data
    )
    return slots_criados