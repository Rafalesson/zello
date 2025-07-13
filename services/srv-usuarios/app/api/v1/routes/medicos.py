# app/api/v1/routes/medicos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud import crud_medico, crud_usuario
from app.schemas import medico as medico_schema
from app.models import usuario as usuario_model
from .auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=medico_schema.MedicoPublic, status_code=status.HTTP_201_CREATED)
def criar_novo_medico(
    medico_in: medico_schema.MedicoCreate,
    db: Session = Depends(get_db),
    current_user: usuario_model.Usuario = Depends(get_current_active_user)
):
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