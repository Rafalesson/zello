# app/api/v1/api.py
from fastapi import APIRouter
from .routes import auth, pacientes, medicos, usuarios

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(pacientes.router, prefix="/pacientes", tags=["Pacientes"])
api_router.include_router(medicos.router, prefix="/medicos", tags=["Médicos"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários (Interno)"])