# app/models/agendamento.py
import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class Agendamento(Base):
    """Representa a reserva de um slot por um paciente."""
    __tablename__ = "agendamentos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slot_id = Column(UUID(as_uuid=True), ForeignKey("slots_de_horario.id"), nullable=False, unique=True)
    # ID do paciente que realizou o agendamento
    paciente_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    
    slot = relationship("SlotDeHorario", back_populates="agendamento")