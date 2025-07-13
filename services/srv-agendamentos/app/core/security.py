# app/core/security.py
from jose import jwt, JWTError
from app.core.config import settings

def decode_access_token(token: str) -> dict | None:
    """
    Decodifica um token de acesso JWT.
    Retorna o payload (dados) se o token for válido, ou None se for inválido.
    """
    try:
        # Decodifica o token usando a mesma chave secreta e algoritmo do srv-usuarios
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None