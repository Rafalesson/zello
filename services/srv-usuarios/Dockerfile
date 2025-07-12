FROM python:3.11-slim

# Define um diretório de trabalho limpo.
WORKDIR /code

# Copia e instala as dependências primeiro para otimizar o cache.
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o contexto do build (incluindo a pasta 'app') para o WORKDIR.
COPY . .

# Expõe a porta.
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]