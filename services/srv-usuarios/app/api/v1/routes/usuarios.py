# app/api/v1/routes/usuarios.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud import crud_usuario
from app.schemas import usuario as usuario_schema
from app.models import usuario as usuario_model

router = APIRouter()

@router.get("/validate/{user_id}", response_model=usuario_schema.UsuarioPublic)
def validate_user_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Endpoint interno para validação de ID de usuário por outros serviços."""
    user = crud_usuario.get(db, user_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou inativo.")
    return user