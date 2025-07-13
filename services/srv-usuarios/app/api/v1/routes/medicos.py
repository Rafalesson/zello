# app/api/v1/routes/medicos.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.crud import crud_medico, crud_usuario
from app.schemas import medico as medico_schema
from app.models import usuario as usuario_model
from .auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[medico_schema.MedicoPublic], summary="Lista todos os Médicos ativos")
def read_medicos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Retorna uma lista de perfis públicos de médicos ativos no sistema."""
    medicos = crud_medico.get_multi(db, skip=skip, limit=limit)
    return medicos

@router.get("/{medico_id}", response_model=medico_schema.MedicoPublic, summary="Busca um Médico por ID")
def read_medico(
    medico_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Retorna o perfil público de um médico específico."""
    db_medico = crud_medico.get(db, medico_id=medico_id)
    if not db_medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return db_medico

@router.post("/", response_model=medico_schema.MedicoPublic, status_code=status.HTTP_201_CREATED, summary="[ADMIN] Cria um novo Médico")
def criar_novo_medico(
    medico_in: medico_schema.MedicoCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    """Cria um novo médico e sua conta de usuário associada."""
    if current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    
    if crud_usuario.get_by_email(db, email=medico_in.usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já está em uso.")
    
    if crud_medico.get_by_crm(db, crm=medico_in.crm):
        raise HTTPException(status_code=400, detail="CRM já está em uso.")

    try:
        medico_data = medico_in.model_dump()
        medico = crud_medico.create_with_usuario(db=db, medico_data=medico_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return medico

@router.put("/{medico_id}", response_model=medico_schema.MedicoPublic, summary="Atualiza um perfil de Médico")
def update_medico(
    medico_id: uuid.UUID,
    medico_in: medico_schema.MedicoUpdate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    """Atualiza as informações de um perfil de médico."""
    medico = crud_medico.get(db, medico_id=medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    if medico.usuario_id != current_user.id and current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    update_data = medico_in.model_dump(exclude_unset=True)
    return crud_medico.update(db=db, db_obj=medico, obj_in=update_data)


@router.delete("/{medico_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desativa um perfil de Médico (Soft Delete)")
def delete_medico(
    medico_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    """Desativa a conta de um médico (soft delete)."""
    medico = crud_medico.get(db, medico_id=medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    if medico.usuario_id != current_user.id and current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    crud_medico.soft_remove(db=db, db_obj=medico)
    return Response(status_code=status.HTTP_204_NO_CONTENT)