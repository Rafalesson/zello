# app/api/v1/routes/agendamentos.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.crud_agendamento import crud_agendamento
from app.schemas import agendamento as agendamento_schema
from .auth import get_current_user_payload
from app.clients.usuario_client import usuario_client

router = APIRouter()

@router.post("/", response_model=agendamento_schema.AgendamentoPublic, status_code=status.HTTP_201_CREATED)
async def create_agendamento(
    agendamento_in: agendamento_schema.AgendamentoCreate,
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_payload)
):
    """Cria um novo agendamento para o paciente autenticado."""
    if current_user_payload.get("tipo_usuario") != "PACIENTE":
        raise HTTPException(status_code=403, detail="Apenas pacientes podem fazer agendamentos.")

    paciente_id = uuid.UUID(current_user_payload.get("user_id"))

    paciente_valido = await usuario_client.validate_user_by_id(paciente_id)
    if not paciente_valido:
        raise HTTPException(status_code=404, detail="Paciente associado ao token é inválido ou inativo.")

    slot = crud_agendamento.get_slot_by_id(db, slot_id=agendamento_in.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Horário não encontrado.")

    try:
        agendamento = crud_agendamento.create_agendamento(db=db, paciente_id=paciente_id, slot=slot)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return agendamento