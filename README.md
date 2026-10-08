# Flash

Personal AI Copilot via WhatsApp.

## Arquitetura atual

WhatsApp Cloud API
-> FastAPI webhook
-> usuário + histórico
-> AgentRuntime
-> LLM com tool calling
-> ToolRegistry
-> PostgreSQL? Não: MySQL
-> scheduler worker
-> WhatsApp

## O que já está implementado

- FastAPI + Uvicorn
- MySQL 8.4 + SQLAlchemy
- Redis
- LLM com tool/function calling
- memória persistente
- histórico de mensagens
- tasks/lembretes persistentes
- scheduler separado
- webhook WhatsApp
- envio de mensagens pela WhatsApp Cloud API
- idempotência por ID da mensagem recebida
- Docker Compose
- testes com pytest
- SQL inicial em database/001_create_schema.sql

## Banco de dados

O Flash usa **MySQL 8.4**.

As tabelas atuais são:

- users
- messages
- memories
- tasks

O SQL está em:

database/001_create_schema.sql

Com Docker, o banco é criado automaticamente pelo serviço mysql.

Para execução manual:

    mysql -u root -p < database/001_create_schema.sql

## Instalação

Requisitos:

- Python 3.11+
- Docker e Docker Compose
- conta WhatsApp Cloud API
- chave de API do provedor LLM

Instale as dependências:

    pip install -e ".[dev]"

Ou, usando o Docker:

    docker compose up --build

## Imports/dependências

Os imports principais usados pelo projeto vêm destes pacotes:

- fastapi
- uvicorn
- pydantic-settings
- sqlalchemy
- pymysql
- redis
- httpx
- openai
- pytest
- pytest-asyncio
- ruff

Não instale psycopg/psycopg2: o banco é MySQL e o driver usado pelo SQLAlchemy é **PyMySQL**.

## Variáveis de ambiente

Copie:

    cp .env.example .env

Preencha:

    DATABASE_URL=mysql+pymysql://flash:flash@localhost:3306/flash?charset=utf8mb4
    REDIS_URL=redis://localhost:6379/0
    LLM_API_KEY=sua-chave
    LLM_MODEL=gpt-5.6
    WHATSAPP_VERIFY_TOKEN=seu-token
    WHATSAPP_ACCESS_TOKEN=seu-token
    WHATSAPP_PHONE_NUMBER_ID=seu-id

Nunca coloque chaves reais no Git.

## Como o agente funciona

Uma mensagem chega pelo WhatsApp:

    WhatsApp
      |
      v
    webhook
      |
      v
    MySQL: salva mensagem
      |
      v
    AgentRuntime
      |
      v
    LLM
      |
      +---- resposta normal
      |
      +---- tool call
                |
                v
            backend valida/executa
                |
                v
              MySQL
                |
                v
          resultado para o LLM
                |
                v
            resposta final
                |
                v
             WhatsApp

O LLM **não possui acesso direto ao banco**. Ele solicita ferramentas; o backend executa as operações.

## Tools atuais

### tasks.create

Cria um lembrete persistente.

Exemplo de intenção:

    Me lembra amanhã às 10h de ligar para Maria.

### tasks.list

Lista tarefas pendentes.

Exemplo:

    Quais são minhas tarefas?

## Segurança

- Não coloque secrets no código.
- Ações destrutivas/sensíveis exigem política de confirmação.
- O backend é responsável por validar e executar tools.
- O LLM nunca deve afirmar que executou uma ação sem resultado real.
- Webhooks usam o ID externo da mensagem para evitar duplicação.

## Rodando localmente

    docker compose up --build

API:

    http://localhost:8000

Health check:

    http://localhost:8000/health

Webhook:

    POST /webhooks/whatsapp

## Próximas etapas

1. confirmação explícita para ações WRITE/DESTRUCTIVE quando necessário
2. parser robusto de datas e timezone para lembretes
3. recorrência de tarefas
4. calendário
5. pesquisa na web
6. áudio/STT
7. e-mail
8. documentos
9. migrations com Alembic
10. observabilidade, rate limiting e hardening
