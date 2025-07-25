# app/schemas/usuario.py
import uuid
import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.usuario import TipoUsuarioEnum

class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str
    tipo_usuario: TipoUsuarioEnum

class UsuarioUpdate(BaseModel):
    """Schema para a atualização de um registro de usuário."""
    is_active: Optional[bool] = None
    foto_perfil_url: Optional[str] = None

class UsuarioPublic(UsuarioBase):
    id: uuid.UUID
    tipo_usuario: TipoUsuarioEnum
    is_active: bool
    data_criacao: datetime.datetime
    foto_perfil_url: Optional[str] = None

    class Config:
        from_attributes = True