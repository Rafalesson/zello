# schemas.py
import uuid
import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Reutilizando o Enum do modelo para consistência
from .models import TipoUsuarioEnum

# ==================
# Schemas de Autenticação
# ==================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ==================
# Schemas de Usuário
# ==================
class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str
    tipo_usuario: TipoUsuarioEnum

class UsuarioPublic(UsuarioBase):
    id: uuid.UUID
    tipo_usuario: TipoUsuarioEnum
    is_active: bool
    data_criacao: datetime.datetime

    class Config:
        from_attributes = True

# ==================
# Schemas de Paciente
# ==================
class PacienteCreate(BaseModel):
    nome_completo: str
    data_nascimento: datetime.date
    telefone: Optional[str] = None
    usuario: UsuarioCreate

class PacientePublic(BaseModel):
    id: uuid.UUID
    nome_completo: str
    data_nascimento: datetime.date
    telefone: Optional[str] = None
    usuario: UsuarioPublic

    class Config:
        from_attributes = True

# ==================
# Schemas de Especialidade
# ==================
class EspecialidadePublic(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# ==================
# Schemas de Médico
# ==================
class MedicoPublic(BaseModel):
    id: uuid.UUID
    nome_completo: str
    crm: str
    especialidades: List[EspecialidadePublic] = []
    usuario: UsuarioPublic

    class Config:
        from_attributes = True