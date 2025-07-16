# app/crud/crud_usuario.py
import uuid
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.models.usuario import Usuario
from app.core.security import get_password_hash

def get_by_email(db: Session, *, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()

def get(db: Session, *, user_id: uuid.UUID) -> Usuario | None:
    """Busca um usuário pelo seu ID."""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create(db: Session, *, user_data: Dict[str, Any]) -> Usuario:
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

def update(db: Session, *, db_obj: Usuario, obj_in: Dict[str, Any]) -> Usuario:
    """Atualiza um registro de usuário a partir de um dicionário."""
    for field, value in obj_in.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj