# app/api/v1/api.py
from fastapi import APIRouter
from .routes import agendas, agendamentos

api_router = APIRouter()

# CORREÇÃO: Adicionando o prefix="/agendas"
api_router.include_router(
    agendas.router, 
    prefix="/agendas", 
    tags=["Agendas e Horários"]
)

api_router.include_router(
    agendamentos.router, 
    prefix="/agendamentos", 
    tags=["Agendamentos"]
)