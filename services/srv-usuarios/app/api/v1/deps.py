# app/api/v1/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database.session import get_db
from app.core.config import settings
from app.crud import crud_usuario
from app.models import usuario as usuario_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: Session = Depends(get_db)
) -> usuario_model.Usuario:
    """
    Dependência principal para decodificar o token e buscar o usuário no banco.
    """
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
    except JWTError:
        raise credentials_exception
    
    user = crud_usuario.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: Annotated[usuario_model.Usuario, Depends(get_current_user)]
) -> usuario_model.Usuario:
    """
    Dependência que garante que o usuário obtido do token está ativo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user