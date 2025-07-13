# app/models/slot_horario.py
import uuid
import enum
from sqlalchemy import Column, DateTime, Enum as PgEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base

class StatusSlotEnum(str, enum.Enum):
    """Define os status possíveis para um slot de horário."""
    DISPONIVEL = "DISPONIVEL"
    AGENDADO = "AGENDADO"
    BLOQUEADO = "BLOQUEADO"

class SlotDeHorario(Base):
    """Representa um bloco de tempo na agenda de um médico."""
    __tablename__ = "slots_de_horario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agenda_id = Column(UUID(as_uuid=True), ForeignKey("agendas.id"), nullable=False)
    horario_inicio = Column(DateTime(timezone=True), nullable=False)
    horario_fim = Column(DateTime(timezone=True), nullable=False)
    status = Column(PgEnum(StatusSlotEnum), nullable=False, default=StatusSlotEnum.DISPONIVEL)

    agenda = relationship("Agenda", back_populates="slots")
    agendamento = relationship("Agendamento", back_populates="slot", uselist=False, cascade="all, delete-orphan")