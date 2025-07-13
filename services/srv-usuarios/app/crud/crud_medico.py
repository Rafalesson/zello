# app/crud/crud_medico.py
import uuid
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.models.medico import Medico
from app.models.especialidade import Especialidade
from app.crud import crud_usuario

def get_by_crm(db: Session, *, crm: str) -> Medico | None:
    """Busca um médico pelo CRM."""
    return db.query(Medico).filter(Medico.crm == crm).first()

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