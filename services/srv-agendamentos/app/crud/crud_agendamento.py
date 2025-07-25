# app/crud/crud_agendamento.py
import uuid
import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.agendamento import Agendamento
from app.models.slot_horario import SlotDeHorario, StatusSlotEnum

class CRUDAgendamento:
    def get_slot_by_id(self, db: Session, slot_id: uuid.UUID) -> Optional[SlotDeHorario]:
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

    # --- NOVA FUNÇÃO ---
    def get_agendamentos_por_paciente(self, db: Session, *, paciente_id: uuid.UUID) -> List[Agendamento]:
        """
        Busca todos os agendamentos (passados e futuros) de um paciente.
        """
        return (
            db.query(Agendamento)
            .join(SlotDeHorario)
            .filter(Agendamento.paciente_id == paciente_id)
            .order_by(SlotDeHorario.horario_inicio.desc()) # Ordena do mais recente para o mais antigo
            .all()
        )
    
    # --- NOVA FUNÇÃO ---
    def get_proximo_agendamento_paciente(self, db: Session, *, paciente_id: uuid.UUID) -> Optional[Agendamento]:
        """
        Busca o próximo agendamento futuro de um paciente.
        """
        return (
            db.query(Agendamento)
            .join(SlotDeHorario)
            .filter(Agendamento.paciente_id == paciente_id)
            .filter(SlotDeHorario.horario_inicio >= datetime.datetime.now(datetime.timezone.utc))
            .order_by(SlotDeHorario.horario_inicio.asc()) # Ordena para pegar o mais próximo
            .first()
        )

crud_agendamento = CRUDAgendamento()