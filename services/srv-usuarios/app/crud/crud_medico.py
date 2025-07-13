# app/crud/crud_medico.py
import uuid
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.core.security import get_password_hash
from app.models.medico import Medico
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.models.especialidade import Especialidade
from app.crud import crud_usuario

def get_by_crm(db: Session, *, crm: str) -> Medico | None:
    """Busca um médico pelo CRM."""
    return db.query(Medico).filter(Medico.crm == crm).first()

def get(db: Session, *, medico_id: uuid.UUID) -> Optional[Medico]:
    """Busca um médico específico pelo seu ID."""
    return db.query(Medico).filter(Medico.id == medico_id, Medico.usuario.has(is_active=True)).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Medico]:
    """Busca uma lista de médicos ativos com paginação."""
    return (
        db.query(Medico)
        .join(Usuario)
        .filter(Usuario.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_with_usuario(db: Session, *, medico_data: Dict[str, Any]) -> Medico:
    
    """Cria um novo médico e seu respectivo usuário a partir de dicionários."""
    usuario_data = medico_data["usuario"]
    db_usuario = crud_usuario.create(db, user_data=usuario_data)

    especialidades = db.query(Especialidade).filter(
        Especialidade.id.in_(medico_data["especialidade_ids"])
    ).all()

    if len(especialidades) != len(medico_data["especialidade_ids"]):
        raise ValueError("Uma ou mais especialidades fornecidas são inválidas.")

    db_medico = Medico(
        id=uuid.uuid4(),
        nome_completo=medico_data["nome_completo"],
        crm=medico_data["crm"],
        foto_perfil_url=medico_data.get("foto_perfil_url"),
        usuario_id=db_usuario.id,
        especialidades=especialidades
    )

    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

def update(db: Session, *, db_obj: Medico, obj_in: Dict[str, Any]) -> Medico:
    """
    Atualiza os dados de um perfil de médico.
    Lida com a atualização de campos simples e da relação com especialidades.
    """
    # Itera sobre os dados de entrada para atualizar os campos do modelo
    for field, value in obj_in.items():
        # A lista de especialidades é tratada separadamente
        if field == "especialidade_ids":
            # Busca os novos objetos de Especialidade no banco de dados
            especialidades = db.query(Especialidade).filter(
                Especialidade.id.in_(value)
            ).all()
            if len(especialidades) != len(value):
                raise ValueError("Uma ou mais especialidades fornecidas são inválidas.")
            # Substitui a lista de especialidades do médico pela nova lista
            db_obj.especialidades = especialidades
        # O usuário é tratado separadamente
        elif field != "usuario":
            setattr(db_obj, field, value)

    # Lida com a atualização do usuário associado, se fornecido
    if "usuario" in obj_in and obj_in.get("usuario"):
        for field, value in obj_in["usuario"].items():
            setattr(db_obj.usuario, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_remove(db: Session, *, db_obj: Medico) -> Medico:
    """
    Realiza a exclusão lógica (soft delete) de um médico, desativando
    sua conta de usuário correspondente.
    """
    # A desativação é feita no registro do usuário associado
    db_obj.usuario.is_active = False
    db.add(db_obj.usuario)
    db.commit()
    db.refresh(db_obj)
    return db_obj