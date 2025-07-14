# app/api/v1/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core import security
from app.schemas import token as token_schema
from app.crud import crud_usuario

router = APIRouter()

@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    Autentica o usuário e retorna um token JWT rico com ID e tipo de usuário.
    """
    user = crud_usuario.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.senha_hash) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos, ou usuário inativo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": user.email,
        "user_id": str(user.id),
        "tipo_usuario": user.tipo_usuario.value
    }
    access_token = security.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}