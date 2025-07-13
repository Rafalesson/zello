# app/models/medico.py
import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base

# Importando a tabela de associação do local correto
from .especialidade import medico_especialidades

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False, unique=True)
    nome_completo = Column(String, nullable=False)
    crm = Column(String, unique=True, index=True, nullable=False)
    foto_perfil_url = Column(String, nullable=True)

    usuario = relationship("Usuario", back_populates="medico")
    especialidades = relationship("Especialidade", secondary=medico_especialidades, back_populates="medicos")
    consultas = relationship("Consulta", back_populates="medico")