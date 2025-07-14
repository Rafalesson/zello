# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# Cria a engine de conexão com o banco de dados
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Dependência do FastAPI para injetar uma sessão de banco de dados em cada requisição.
    Garante que a sessão seja sempre fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()