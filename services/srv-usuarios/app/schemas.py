from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

# --- Schema Base ---
# Atributos que são compartilhados por outros schemas
class PacienteBase(BaseModel):
    email: EmailStr
    nome_completo: str
    data_nascimento: datetime.date
    telefone: Optional[str] = None


# --- Schema para Criação ---
# Atributos necessários para criar um novo paciente (recebidos pela API)
class PacienteCreate(PacienteBase):
    senha: str


# --- Schema para Leitura/Resposta ---
# Atributos que serão retornados pela API (protegendo dados sensíveis)
class PacientePublic(PacienteBase):
    id: int
    is_active: bool
    data_criacao: datetime.datetime

    class Config:
        # Ajuda o Pydantic a converter o modelo SQLAlchemy (que é um objeto) em um dicionário (JSON)
        from_attributes = True