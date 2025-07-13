# app/api/v1/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database.session import get_db
from app.core import security
from app.core.config import settings
from app.schemas import token as token_schema
from app.crud import crud_usuario
from app.models import usuario as usuario_model

router = APIRouter()

# O tokenUrl agora aponta para o caminho completo do endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Esta dependência agora é local para o módulo de autenticação
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Session = Depends(get_db)
) -> usuario_model.Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = token_schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud_usuario.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Esta dependência pode ser importada por outras rotas
def get_current_active_user(
    current_user: Annotated[usuario_model.Usuario, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = crud_usuario.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.senha_hash) or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos, ou usuário inativo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}