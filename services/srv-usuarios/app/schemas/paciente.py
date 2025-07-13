# app/schemas/paciente.py
import uuid
import datetime
from pydantic import BaseModel
from typing import Optional
from .usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate

class PacienteBase(BaseModel):
    nome_completo: str
    data_nascimento: datetime.date
    telefone: Optional[str] = None

class PacienteCreate(PacienteBase):
    usuario: UsuarioCreate

class PacienteUpdate(BaseModel):
    nome_completo: Optional[str] = None
    data_nascimento: Optional[datetime.date] = None
    telefone: Optional[str] = None
    usuario: Optional[UsuarioUpdate] = None

class PacientePublic(PacienteBase):
    id: uuid.UUID
    usuario: UsuarioPublic

    class Config:
        from_attributes = True