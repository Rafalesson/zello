# crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import uuid

# Configuração para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Retorna o hash de uma senha em texto plano."""
    return pwd_context.hash(password)

def get_usuario_by_email(db: Session, email: str) -> models.Usuario | None:
    """Busca um usuário pelo seu e-mail."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def criar_paciente(db: Session, paciente_data: schemas.PacienteCreate) -> models.Paciente:
    """
    Cria um novo registro de Usuário e um registro de Paciente associado.
    Tudo dentro de uma única transação.
    """
    # Extrai os dados do usuário do schema aninhado
    usuario_data = paciente_data.usuario
    
    # Cria o hash da senha
    hashed_senha = get_password_hash(usuario_data.senha)
    
    # Cria a instância do modelo de Usuário
    db_usuario = models.Usuario(
        email=usuario_data.email,
        senha_hash=hashed_senha,
        tipo_usuario=usuario_data.tipo_usuario,
    )

    # Cria a instância do modelo de Paciente
    db_paciente = models.Paciente(
        id=uuid.uuid4(),  # Gerar um UUID para o paciente
        nome_completo=paciente_data.nome_completo,
        data_nascimento=paciente_data.data_nascimento,
        telefone=paciente_data.telefone,
        # Associa o perfil do paciente ao usuário
        usuario=db_usuario
    )

    db.add(db_paciente) # Adicionar o paciente também adiciona o usuário devido ao 'cascade'
    db.commit()
    db.refresh(db_paciente)
    
    return db_paciente