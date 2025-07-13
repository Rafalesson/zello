# app/schemas/agendamento.py
import uuid
import datetime
from pydantic import BaseModel
from .slot_horario import SlotHorarioPublic

class AgendamentoCreate(BaseModel):
    """Schema de entrada para criar um novo agendamento."""
    slot_id: uuid.UUID

class AgendamentoPublic(BaseModel):
    """Representação pública de um agendamento."""
    id: uuid.UUID
    paciente_id: uuid.UUID
    data_criacao: datetime.datetime
    slot: SlotHorarioPublic # Inclui os detalhes do horário agendado

    class Config:
        from_attributes = True