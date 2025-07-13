# app/schemas/especialidade.py
from pydantic import BaseModel

class EspecialidadeBase(BaseModel):
    nome: str

class EspecialidadePublic(EspecialidadeBase):
    id: int

    class Config:
        from_attributes = True