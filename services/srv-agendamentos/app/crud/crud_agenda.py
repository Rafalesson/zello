# app/crud/crud_agenda.py
import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func  # <-- IMPORTAÇÃO ADICIONADA
from typing import List, Optional, Dict, Any

from app.models.agenda import Agenda
from app.models.slot_horario import SlotDeHorario, StatusSlotEnum

def get_or_create_agenda(db: Session, *, medico_id: uuid.UUID) -> Agenda:
    """
    Busca uma agenda pelo ID do médico. Se não existir, cria uma nova.
    Garante que cada médico tenha apenas uma agenda.
    """
    agenda = db.query(Agenda).filter(Agenda.medico_id == medico_id).first()
    
    if not agenda:
        agenda = Agenda(id=uuid.uuid4(), medico_id=medico_id)
        db.add(agenda)
        db.commit()
        db.refresh(agenda)
    return agenda

def create_slots_para_agenda(db: Session, *, agenda: Agenda, slots_data: List[Dict[str, Any]]) -> List[SlotDeHorario]:
    """
    Cria múltiplos slots de horário para uma agenda específica.
    """
    slots_criados = []
    for slot_info in slots_data:
        db_slot = SlotDeHorario(
            id=uuid.uuid4(),
            agenda_id=agenda.id,
            horario_inicio=slot_info['horario_inicio'],
            horario_fim=slot_info['horario_fim']
        )
        slots_criados.append(db_slot)
    
    db.add_all(slots_criados)
    db.commit()
    for slot in slots_criados:
        db.refresh(slot)
        
    return slots_criados

def get_slots_disponiveis(
    db: Session, *, medico_id: uuid.UUID, data: Optional[datetime.date] = None
) -> List[SlotDeHorario]:
    """
    Busca os slots de horário disponíveis para um médico específico.
    - Filtra por status "DISPONIVEL".
    - Opcionalmente, filtra por uma data específica de forma segura.
    """
    query = (
        db.query(SlotDeHorario)
        .join(Agenda)
        .filter(Agenda.medico_id == medico_id)
        .filter(SlotDeHorario.status == StatusSlotEnum.DISPONIVEL)
    )

    if data:
        # Agora o 'func' é reconhecido pelo Python
        query = query.filter(func.date(SlotDeHorario.horario_inicio) == data)
        
    return query.order_by(SlotDeHorario.horario_inicio).all()