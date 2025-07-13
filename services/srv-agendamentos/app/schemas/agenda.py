# app/schemas/agenda.py
import uuid
from pydantic import BaseModel
from typing import List
from .slot_horario import SlotHorarioPublic

class AgendaBase(BaseModel):
    """Schema base para a agenda, contendo o ID do médico."""
    medico_id: uuid.UUID

class AgendaPublic(AgendaBase):
    """Representação pública de uma agenda, incluindo seus slots."""
    id: uuid.UUID
    slots: List[SlotHorarioPublic] = []

    class Config:
        from_attributes = True