# app/models/__init__.py

# Importa a Base do nosso session.py para que todos os modelos a usem
from app.database.session import Base

# Importa todas as classes de modelo
# A ordem aqui não importa, pois o Python irá resolver as dependências
# após carregar todos eles neste namespace.
from .usuario import Usuario
from .paciente import Paciente
from .medico import Medico
from .especialidade import Especialidade
from .consulta import Consulta