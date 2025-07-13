# app/schemas/medico.py
import uuid
from pydantic import BaseModel
from typing import Optional, List
from .usuario import UsuarioCreate, UsuarioPublic, UsuarioUpdate
from .especialidade import EspecialidadePublic

class MedicoBase(BaseModel):
    nome_completo: str
    crm: str
    foto_perfil_url: Optional[str] = None

class MedicoCreate(MedicoBase):
    especialidade_ids: List[int]
    usuario: UsuarioCreate

class MedicoUpdate(BaseModel):
    nome_completo: Optional[str] = None
    foto_perfil_url: Optional[str] = None
    especialidade_ids: Optional[List[int]] = None
    usuario: Optional[UsuarioUpdate] = None

class MedicoPublic(MedicoBase):
    id: uuid.UUID
    especialidades: List[EspecialidadePublic] = []
    usuario: UsuarioPublic

    class Config:
        from_attributes = True