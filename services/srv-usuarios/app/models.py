import uuid
import enum
from sqlalchemy import (Boolean, Column, Integer, String, Date, DateTime, 
                        ForeignKey, Table, Enum as PgEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .database import Base

# ENUM para os tipos de usuário, garantindo consistência
class TipoUsuarioEnum(str, enum.Enum):
    PACIENTE = 'PACIENTE'
    MEDICO = 'MEDICO'
    ADMIN = 'ADMIN'

# Tabela de associação para o relacionamento Muitos-para-Muitos entre Médico e Especialidade
medico_especialidades = Table(
    'medico_especialidades', Base.metadata,
    Column('medico_id', UUID(as_uuid=True), ForeignKey('medicos.id'), primary_key=True),
    Column('especialidade_id', Integer, ForeignKey('especialidades.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    tipo_usuario = Column(PgEnum(TipoUsuarioEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    ultimo_login = Column(DateTime(timezone=True), nullable=True)

    paciente = relationship("Paciente", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    medico = relationship("Medico", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False, unique=True)
    nome_completo = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String, nullable=True)
    
    usuario = relationship("Usuario", back_populates="paciente")
    consultas = relationship("Consulta", back_populates="paciente")

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

class Especialidade(Base):
    __tablename__ = "especialidades"
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    
    medicos = relationship("Medico", secondary=medico_especialidades, back_populates="especialidades")

class Consulta(Base):
    __tablename__ = "consultas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey('pacientes.id'), nullable=False, index=True)
    medico_id = Column(UUID(as_uuid=True), ForeignKey('medicos.id'), nullable=False, index=True)
    data_hora_agendamento = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default='AGENDADA', nullable=False) # Simplificado para String por enquanto
    link_sala_virtual = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")