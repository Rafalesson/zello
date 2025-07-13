# app/crud/crud_usuario.py
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.models.usuario import Usuario
from app.core.security import get_password_hash

def get_by_email(db: Session, *, email: str) -> Usuario | None:
    """Busca um usuário pelo seu e-mail."""
    return db.query(Usuario).filter(Usuario.email == email).first()

def create(db: Session, *, user_data: Dict[str, Any]) -> Usuario: # <-- Parâmetro corrigido de 'user_in' para 'user_data'
    """Cria um novo usuário base a partir de um dicionário."""
    hashed_password = get_password_hash(user_data["senha"])
    db_obj = Usuario(
        email=user_data["email"],
        senha_hash=hashed_password,
        tipo_usuario=user_data["tipo_usuario"]
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj