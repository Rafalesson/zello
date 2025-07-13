# app/api/v1/routes/agendamentos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.crud_agendamento import crud_agendamento
from app.schemas import agendamento as agendamento_schema
from .auth import get_current_user_payload

router = APIRouter()

@router.post("/", response_model=agendamento_schema.AgendamentoPublic, status_code=status.HTTP_201_CREATED)
def create_agendamento(
    *,
    db: Session = Depends(get_db),
    agendamento_in: agendamento_schema.AgendamentoCreate,
    current_user: dict = Depends(get_current_user_payload)
):
    """
    Cria um novo agendamento para o paciente autenticado.
    """
    # Futuramente, usaríamos o e-mail para buscar o paciente_id no srv-usuarios
    # Por enquanto, vamos simular que o ID do paciente é o mesmo do usuário.
    # Esta é uma simplificação temporária.
    paciente_email = current_user.get("sub")
    # Simulação: Precisaríamos de um endpoint em srv-usuarios para nos dar o ID do paciente a partir do email.
    # Vamos usar um ID fixo para o teste.
    paciente_id_fixo = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11" # Use o ID de um paciente que vc criou
    
    slot = crud_agendamento.get_slot_by_id(db, slot_id=agendamento_in.slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Horário não encontrado.")

    try:
        agendamento = crud_agendamento.create_agendamento(db=db, paciente_id=paciente_id_fixo, slot=slot)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return agendamento