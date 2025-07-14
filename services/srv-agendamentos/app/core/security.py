# app/core/security.py (no srv-agendamentos)
from jose import jwt, JWTError
from app.core.config import settings

def decode_access_token(token: str) -> dict | None:
    """
    Decodifica um token de acesso JWT.

    Verifica a assinatura e a validade do token usando a mesma chave secreta
    e algoritmo do serviço de usuários.

    Retorna:
        O payload (dicionário com os dados) se o token for válido, ou None.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None