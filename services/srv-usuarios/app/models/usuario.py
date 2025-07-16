# app/models/usuario.py
import uuid, enum
from sqlalchemy import Boolean, Column, String, DateTime, Enum as PgEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.session import Base

class TipoUsuarioEnum(str, enum.Enum):
    PACIENTE = 'PACIENTE'
    MEDICO = 'MEDICO'
    ADMIN = 'ADMIN'

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    foto_perfil_url = Column(String, nullable=True)
    tipo_usuario = Column(PgEnum(TipoUsuarioEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    ultimo_login = Column(DateTime(timezone=True), nullable=True)

    paciente = relationship("Paciente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    medico = relationship("Medico", back_populates="usuario", uselist=False, cascade="all, delete-orphan")