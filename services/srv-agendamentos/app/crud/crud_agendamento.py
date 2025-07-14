# app/crud/crud_agendamento.py
import uuid
from sqlalchemy.orm import Session

from app.models.agendamento import Agendamento
from app.models.slot_horario import SlotDeHorario, StatusSlotEnum

class CRUDAgendamento:
    def get_slot_by_id(self, db: Session, slot_id: uuid.UUID) -> SlotDeHorario | None:
        """Busca um slot de horário específico pelo ID."""
        return db.query(SlotDeHorario).filter(SlotDeHorario.id == slot_id).first()

    def create_agendamento(self, db: Session, *, paciente_id: uuid.UUID, slot: SlotDeHorario) -> Agendamento:
        """
        Cria um novo agendamento e atualiza o status do slot.
        Esta operação deve ser atômica.
        """
        if slot.status != StatusSlotEnum.DISPONIVEL:
            raise ValueError("Este horário não está mais disponível.")

        slot.status = StatusSlotEnum.AGENDADO
        
        db_agendamento = Agendamento(
            id=uuid.uuid4(),
            slot_id=slot.id,
            paciente_id=paciente_id
        )
        
        db.add(slot)
        db.add(db_agendamento)
        db.commit()
        db.refresh(db_agendamento)
        
        return db_agendamento

crud_agendamento = CRUDAgendamento()