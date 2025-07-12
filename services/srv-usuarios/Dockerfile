# Dockerfile para serviços FastAPI

# Usamos uma imagem base específica e leve para builds consistentes.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Copia e instala as dependências antes do código da aplicação para otimizar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho.
COPY . .

# Expõe a porta que o Uvicorn usará.
EXPOSE 8000

# Comando para iniciar o servidor. O host 0.0.0.0 torna o serviço acessível a partir de outros containers.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]