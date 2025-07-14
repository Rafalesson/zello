# app/schemas/token.py
from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    """Schema para os dados contidos dentro de um token JWT."""
    email: Optional[str] = None