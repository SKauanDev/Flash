# Flash

Personal AI Copilot via WhatsApp.

## Ambiente recomendado: Windows + XAMPP + MySQL

O Flash **não precisa de Docker**.

Use:

- Windows
- Python 3.11+
- XAMPP com MySQL
- Redis local
- WhatsApp Cloud API
- API de LLM

## 1. Instalar dependências Python

Na pasta do projeto:

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -e ".[dev]"

O projeto configura o setuptools para incluir somente o pacote Python `app`. A pasta `database` não é um pacote Python, portanto o erro "Multiple top-level packages discovered" não deve mais ocorrer.

## 2. Configurar XAMPP

1. Abra o XAMPP Control Panel.
2. Inicie **MySQL**.
3. Confirme que o MySQL está na porta **3306**.
4. O Apache não é necessário para executar o Flash.
5. Redis também precisa estar disponível localmente.

Se o usuário root do XAMPP não tiver senha, o script de setup já está configurado para isso.

## 3. Criar o banco MySQL

O SQL está em:

    database/001_create_schema.sql

Você pode executar pelo phpMyAdmin ou pelo script:

    python scripts/setup_database.py

O banco cria:

- users
- messages
- memories
- tasks

## 4. Configurar o ambiente

Copie:

    copy .env.example .env

Configure:

    DATABASE_URL=mysql+pymysql://flash:flash@127.0.0.1:3306/flash?charset=utf8mb4
    REDIS_URL=redis://127.0.0.1:6379/0
    LLM_API_KEY=sua_chave
    LLM_MODEL=gpt-5.6
    WHATSAPP_VERIFY_TOKEN=seu_token
    WHATSAPP_ACCESS_TOKEN=seu_token
    WHATSAPP_PHONE_NUMBER_ID=seu_id

Nunca coloque chaves reais no Git.

## 5. Pacotes/imports usados

Principais dependências:

- `fastapi` — API/webhook
- `uvicorn` — servidor
- `pydantic-settings` — configuração
- `sqlalchemy` — ORM
- `pymysql` — driver MySQL
- `redis` — Redis
- `httpx` — chamadas HTTP
- `openai` — integração LLM
- `pytest` — testes
- `pytest-asyncio` — testes assíncronos
- `ruff` — lint

Não é necessário instalar `psycopg` ou `psycopg2`.

## 6. Executar a API

Com o ambiente virtual ativo:

    uvicorn app.main:app --reload

API:

    http://127.0.0.1:8000

Teste:

    http://127.0.0.1:8000/health

## 7. Executar o scheduler

Em outro terminal, com o ambiente virtual ativo:

    python scripts/run_worker.py

O worker verifica tarefas vencidas e envia o lembrete pelo WhatsApp.

## Arquitetura

    WhatsApp
       |
       v
    FastAPI webhook
       |
       v
    MySQL: usuário + mensagem
       |
       v
    AgentRuntime
       |
       v
    LLM + tool calling
       |
       +---- resposta normal
       |
       +---- tasks.create / tasks.list
                  |
                  v
                MySQL
                  |
                  v
              scheduler
                  |
                  v
               WhatsApp

O LLM não acessa o banco diretamente. Ele solicita uma tool e o backend executa a operação.

## Tools atuais

### tasks.create

Cria um lembrete persistente.

### tasks.list

Lista tarefas pendentes.

## Estrutura importante

    Flash/
    ├── app/
    │   ├── agent/
    │   ├── api/
    │   ├── db/
    │   ├── memory/
    │   ├── scheduler/
    │   ├── services/
    │   ├── tools/
    │   └── whatsapp/
    ├── database/
    │   └── 001_create_schema.sql
    ├── scripts/
    │   ├── setup_database.py
    │   └── run_worker.py
    ├── tests/
    ├── .env.example
    └── pyproject.toml

## Próximas etapas

1. Resolver datas relativas e timezone no `tasks.create`.
2. Confirmação para ações WRITE/DESTRUCTIVE.
3. Tarefas recorrentes.
4. Calendário.
5. Pesquisa web.
6. Áudio/STT.
7. E-mail.
8. Documentos.
9. Migrations.
10. Observabilidade e hardening.
