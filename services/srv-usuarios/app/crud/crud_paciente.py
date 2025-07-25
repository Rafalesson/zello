# app/crud/crud_paciente.py
import uuid
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.models.paciente import Paciente
from app.models.usuario import Usuario
from app.crud import crud_usuario

def get(db: Session, *, paciente_id: uuid.UUID) -> Optional[Paciente]:
    """Busca um paciente específico pelo seu ID."""
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Paciente]:
    """
    Busca uma lista de pacientes, retornando APENAS os que estão ativos.
    """
    return (
        db.query(Paciente)
        .join(Usuario)
        .filter(Usuario.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_by_usuario_id(db: Session, *, usuario_id: uuid.UUID) -> Optional[Paciente]:
    """Busca um perfil de paciente pelo ID do usuário associado."""
    return db.query(Paciente).filter(Paciente.usuario_id == usuario_id).first()

def create_with_usuario(db: Session, *, paciente_data: Dict[str, Any]) -> Paciente:
    """Cria um novo paciente e seu respectivo usuário a partir de dicionários."""
    usuario_data = paciente_data["usuario"]
    db_usuario = crud_usuario.create(db, user_data=usuario_data)

    db_paciente = Paciente(
        id=uuid.uuid4(),
        nome_completo=paciente_data["nome_completo"],
        data_nascimento=paciente_data["data_nascimento"],
        telefone=paciente_data.get("telefone"),
        usuario_id=db_usuario.id
    )

    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def update(db: Session, *, db_obj: Paciente, obj_in: Dict[str, Any]) -> Paciente:
    """Atualiza os dados de um paciente a partir de um dicionário."""
    # Converte o Pydantic model para um dicionário, excluindo valores não setados
    update_data = obj_in

    for key, value in update_data.items():
        if key != "usuario":
            setattr(db_obj, key, value)
    
    if "usuario" in update_data and update_data.get("usuario"):
        for key, value in update_data["usuario"].items():
            setattr(db_obj.usuario, key, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_remove(db: Session, *, db_obj: Paciente) -> Paciente:
    """Realiza a exclusão lógica (soft delete) de um paciente."""
    db_obj.usuario.is_active = False
    db.add(db_obj.usuario)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def hard_remove(db: Session, *, db_obj: Paciente):
    """Realiza a exclusão física (hard delete) de um paciente."""
    db.delete(db_obj)
    db.commit()
    return