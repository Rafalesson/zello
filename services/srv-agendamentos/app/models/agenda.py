# app/models/agenda.py
import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base

class Agenda(Base):
    """Representa a agenda de um profissional de saúde."""
    __tablename__ = "agendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Referência ao ID do médico no serviço de usuários. Não é uma FK de banco,
    # mas uma chave lógica para conectar os serviços.
    medico_id = Column(UUID(as_uuid=True), index=True, nullable=False, unique=True)

    # Relacionamento com os slots de horário
    slots = relationship("SlotDeHorario", back_populates="agenda", cascade="all, delete-orphan")