# 🩺 Projeto Zello - Plataforma de Telemedicina

![Zello Home Page](https://i.imgur.com/your-screenshot-url.png) **Zello** é uma plataforma de telemedicina moderna e distribuída, projetada para conectar pacientes e médicos de forma simples, segura e eficiente. [cite_start]O projeto foi desenvolvido como parte da disciplina de Sistemas Distribuídos, com foco em arquitetura de microsserviços, comunicação assíncrona e práticas modernas de desenvolvimento. [cite: 4, 11]

---

## 🏛️ Arquitetura

[cite_start]O sistema é construído sobre uma arquitetura de microsserviços, onde cada serviço possui uma responsabilidade única e um banco de dados isolado, garantindo alta coesão e baixo acoplamento. [cite: 12]

- **`api-gateway` (Go & Gin):** O ponto de entrada único para todas as requisições do frontend. Atua como um Proxy Reverso, roteirando o tráfego para os serviços internos apropriados e gerenciando a política de CORS.
- **`srv-usuarios` (Python & FastAPI):** Responsável por toda a gestão de identidade: cadastro, login, perfis de pacientes, médicos e administradores. É a "fonte da verdade" sobre quem são os usuários.
- **`srv-agendamentos` (Python & FastAPI):** Gerencia a lógica de negócio principal da plataforma, incluindo agendas dos médicos, criação de horários disponíveis e o agendamento de consultas.
- **`app-frontend` (Next.js & React):** A interface gráfica com a qual os usuários interagem. [cite_start]É um módulo independente que consome a API através do Gateway. [cite: 15]
- [cite_start]**`rabbitmq` (Message Broker):** Prepara o sistema para comunicação assíncrona entre os serviços, permitindo que eventos (como "consulta agendada") sejam processados por diferentes partes do sistema de forma desacoplada. [cite: 16]
- **Bancos de Dados (PostgreSQL):** Cada serviço principal possui sua própria instância de banco de dados PostgreSQL, garantindo o isolamento total dos dados.

[cite_start]Todos os serviços são containerizados usando **Docker** e orquestrados localmente com **Docker Compose**. [cite: 18]

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python (FastAPI), Go (Gin)
- **Frontend:** Next.js (React), TypeScript, Tailwind CSS
- **Banco de Dados:** PostgreSQL
- **Mensageria:** RabbitMQ
- **Containerização:** Docker, Docker Compose
- **Gestão de Dependências:** Poetry (Python), Go Modules, NPM (Node.js)

---

## 🚀 Como Executar e Testar

Siga estes passos para configurar e executar o ambiente de desenvolvimento localmente.

### 1. Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/) (para o frontend)
- [Go](https://go.dev/doc/install) (para o gateway)
- [Python](https://www.python.org/downloads/) (para os serviços de backend)

### 2. Configuração do Ambiente

**a. Clone o Repositório**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd zello