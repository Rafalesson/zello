# models.py

from sqlalchemy import Boolean, Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from .database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nome_completo = Column(String, nullable=False)
    
    hashed_senha = Column(String, nullable=False)

    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())