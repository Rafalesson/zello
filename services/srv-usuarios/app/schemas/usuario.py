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
    is_active: Optional[bool] = None

class UsuarioPublic(UsuarioBase):
    id: uuid.UUID
    tipo_usuario: TipoUsuarioEnum
    is_active: bool
    data_criacao: datetime.datetime

    class Config:
        from_attributes = True