# app/models/especialidade.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from app.database.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# Esta é a tabela de associação que estava faltando.
# Ela define a relação muitos-para-muitos.
medico_especialidades = Table(
    'medico_especialidades', Base.metadata,
    Column('medico_id', UUID(as_uuid=True), ForeignKey('medicos.id'), primary_key=True),
    Column('especialidade_id', Integer, ForeignKey('especialidades.id'), primary_key=True)
)

class Especialidade(Base):
    __tablename__ = "especialidades"
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)

    medicos = relationship("Medico", secondary=medico_especialidades, back_populates="especialidades")