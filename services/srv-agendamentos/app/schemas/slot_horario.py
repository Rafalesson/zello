# app/schemas/slot_horario.py
import uuid
import datetime
from pydantic import BaseModel, Field
from typing import List
from app.models.slot_horario import StatusSlotEnum

class SlotHorarioBase(BaseModel):
    """Schema base com os campos essenciais de um slot de horário."""
    horario_inicio: datetime.datetime
    horario_fim: datetime.datetime

class SlotHorarioCreate(SlotHorarioBase):
    """Schema usado para a criação de novos slots. Não precisa de mais campos."""
    pass

class SlotHorarioPublic(SlotHorarioBase):
    """Schema para representar um slot publicamente, incluindo seu ID e status."""
    id: uuid.UUID
    status: StatusSlotEnum

    class Config:
        from_attributes = True

class SlotsParaCriacao(BaseModel):
    """
    Schema de entrada para o endpoint de criação de múltiplos slots.
    Espera uma lista de objetos SlotHorarioCreate.
    """
    slots: List[SlotHorarioCreate] = Field(..., min_length=1)