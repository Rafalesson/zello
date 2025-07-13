# app/models/consulta.py
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base

class Consulta(Base):
    """
    Representa uma consulta agendada no sistema.
    Conecta um Paciente a um Médico em um horário específico.
    """
    __tablename__ = "consultas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    paciente_id = Column(UUID(as_uuid=True), ForeignKey('pacientes.id'), nullable=False, index=True)
    medico_id = Column(UUID(as_uuid=True), ForeignKey('medicos.id'), nullable=False, index=True)
    
    data_hora_agendamento = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default='AGENDADA', nullable=False) # Ex: AGENDADA, REALIZADA, CANCELADA
    link_sala_virtual = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")