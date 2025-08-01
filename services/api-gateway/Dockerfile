# Dockerfile para o serviço em Go usando Multi-Stage Build

# --- Estágio de Build ---
# CORREÇÃO: Atualizamos a versão do Go para a 1.23, conforme exigido pelo go.mod
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Copia os arquivos de gerenciamento de dependências.
COPY go.mod ./
COPY go.sum ./

# Baixa as dependências.
RUN go mod download

# Copia o código fonte.
COPY . .

# Compila a aplicação, criando um binário estático.
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o api-gateway .

# --- Estágio de Produção ---
# Usamos a imagem 'scratch', que é vazia, para a imagem final.
FROM scratch

WORKDIR /root/

# Copia o binário compilado do estágio de build.
COPY --from=builder /app/api-gateway .

# Expõe a porta que a aplicação usará.
EXPOSE 8080

# Comando para executar o binário.
CMD ["./api-gateway"]