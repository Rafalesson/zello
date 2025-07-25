# app/api/v1/routes/pacientes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud import crud_paciente, crud_usuario
from app.schemas import paciente as paciente_schema
from app.models import usuario as usuario_model
from app.api.v1.deps import get_current_active_user

router = APIRouter()

@router.post("/", response_model=paciente_schema.PacientePublic, status_code=status.HTTP_201_CREATED)
def criar_novo_paciente(
    paciente_in: paciente_schema.PacienteCreate,
    db: Session = Depends(get_db)
):
    if crud_usuario.get_by_email(db, email=paciente_in.usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já está em uso.")
    
    paciente_data = paciente_in.model_dump()
    return crud_paciente.create_with_usuario(db=db, paciente_data=paciente_data)

@router.get("/{usuario_id}", response_model=paciente_schema.PacientePublic, summary="Busca um Paciente por ID de Usuário")
def read_paciente(
    usuario_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    """
    Retorna os dados de um paciente específico, buscando pelo ID do usuário.
    **Acesso: O próprio paciente ou administradores.**
    """
    # Lógica de Autorização: Garante que o usuário logado só pode buscar seu próprio perfil (a menos que seja admin)
    if (current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN and 
        current_user.id != usuario_id):
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    
    # Usa a nova função de busca
    paciente = crud_paciente.get_by_usuario_id(db, usuario_id=usuario_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Perfil de paciente não encontrado para este usuário")
    
    return paciente

@router.put("/{paciente_id}", response_model=paciente_schema.PacientePublic)
def update_paciente(
    paciente_id: uuid.UUID,
    paciente_in: paciente_schema.PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    paciente = crud_paciente.get(db, paciente_id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN and paciente.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    
    update_data = paciente_in.model_dump(exclude_unset=True)
    return crud_paciente.update(db=db, db_obj=paciente, obj_in=update_data)

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paciente(
    paciente_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    paciente = crud_paciente.get(db, paciente_id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN and paciente.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    crud_paciente.soft_remove(db=db, db_obj=paciente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/admin/{paciente_id}/force", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_paciente(
    paciente_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
    if current_user.tipo_usuario != usuario_model.TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    paciente = crud_paciente.get(db, paciente_id=paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    crud_paciente.hard_remove(db=db, db_obj=paciente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)