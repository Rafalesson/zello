# app/crud/crud_medico.py
import uuid
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from app.core.security import get_password_hash
from app.models.medico import Medico
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.models.especialidade import Especialidade
from app.crud import crud_usuario

def get(db: Session, *, medico_id: uuid.UUID) -> Optional[Medico]:
    """Busca um médico específico pelo seu ID de perfil."""
    return db.query(Medico).filter(Medico.id == medico_id).first()

def get_by_usuario_id(db: Session, *, usuario_id: uuid.UUID) -> Optional[Medico]:
    """Busca um perfil de médico pelo ID do usuário associado."""
    return db.query(Medico).filter(Medico.usuario_id == usuario_id).first()

def get_by_crm(db: Session, *, crm: str) -> Medico | None:
    """Busca um médico pelo CRM."""
    return db.query(Medico).filter(Medico.crm == crm).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Medico]:
    """Busca uma lista de médicos ativos com paginação."""
    return db.query(Medico).join(Usuario).filter(Usuario.is_active == True).offset(skip).limit(limit).all()

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
    """Atualiza os dados de um perfil de médico."""
    if "especialidade_ids" in obj_in:
        especialidades = db.query(Especialidade).filter(
            Especialidade.id.in_(obj_in["especialidade_ids"])
        ).all()
        if len(especialidades) != len(obj_in["especialidade_ids"]):
            raise ValueError("Uma ou mais especialidades fornecidas são inválidas.")
        db_obj.especialidades = especialidades
        del obj_in["especialidade_ids"]

    # Itera sobre os dados de entrada para atualizar o objeto do banco
    update_data = obj_in.copy()
    if "usuario" in update_data:
        del update_data["usuario"] # Remove para tratar separadamente

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    # Lida com a atualização do usuário associado, se houver
    if "usuario" in obj_in and obj_in.get("usuario"):
        for field, value in obj_in["usuario"].items():
            setattr(db_obj.usuario, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj