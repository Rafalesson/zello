# crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Configuração para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def criar_paciente(db: Session, paciente: schemas.PacienteCreate) -> models.Paciente:
    """
    Cria um novo paciente no banco de dados.
    """
    hashed_senha = get_password_hash(paciente.senha)
    
    db_paciente = models.Paciente(
        email=paciente.email,
        nome_completo=paciente.nome_completo,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        hashed_senha=hashed_senha
    )
    
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente