# app/api/v1/routes/auth.py (no srv-agendamentos)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.core.config import settings
from app.schemas.token import TokenData # Criaremos este schema a seguir

# O tokenUrl apenas informa à documentação Swagger onde o login acontece (no outro serviço).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"http://localhost:8001{settings.API_V1_STR}/auth/login") 

def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependência para obter o payload do token do usuário atual.
    Valida o token e extrai seus dados.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload