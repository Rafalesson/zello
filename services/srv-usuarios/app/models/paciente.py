# app/models/paciente.py
import uuid
from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False, unique=True)
    nome_completo = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String, nullable=True)
    
    usuario = relationship("Usuario", back_populates="paciente")
    consultas = relationship("Consulta", back_populates="paciente")